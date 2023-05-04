#!/usr/bin/env python

import os
import argparse

import requests
import codecs
from tqdm import tqdm
import zipfile, io

from prefect import task, flow
from pathlib import Path

project_id = 'final-385014'

@task(log_prints=True, name="Query Wmata API for static gtfs data", retries=3)
def query_gtfs_api(api_key: str = os.environ['WMATA_KEY'], api_url: str = "https://api.wmata.com/gtfs/bus-gtfs-static.zip") -> bytes:

    headers = {
        # Request headers
        'api_key': api_key,
    }

    def download(url: str, headers):
        resp = requests.get(url, headers=headers, stream=True)
        total = int(resp.headers.get('content-length', 0))
        with tqdm(
            desc=url,
            total=total,
            unit='b',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in resp.iter_content(chunk_size=65536):
                bar.update(len(chunk))
                yield chunk

    try:
        bio = io.BytesIO()
        for chunk in download(api_url, headers):
            bio.write(chunk)
        return bio.getvalue()

    except requests.exceptions.RequestException as e:
        print("[Requests error ]", e)

#'https://api.wmata.com/gtfs/bus-gtfs-static.zip'

@task(log_prints=True, name="Unzip gtfs static data", retries=3)
def unzip_file(content: bytes, extract_dir: Path="gtfs", retries=3)-> None:
    
    print("unzipping........")
    try:
        with zipfile.ZipFile(io.BytesIO(content),"r") as zip_ref:
            zip_ref.extractall(extract_dir)
        print("Successfully unzip data.")
        #split large file for bq ingestion
        os.system('tail -n +2 stop_times.txt | split -d --line-bytes=100M - stop_chunk_')
    except BadZipfile:
        print("Wmata gtfs static data failed")

@task(log_prints=True, name="Query Wmata API for json stops data", retries=3)
def query_stops_json(api_key: str = os.environ['WMATA_KEY'], api_url: str = "https://api.wmata.com/Bus.svc/json/jStops", extract_dir: Path="gtfs") -> bytes:

    headers = {
        # Request headers
        'api_key': api_key,
    }

    try:
        r = requests.get(api_url, headers = headers)
        with codecs.open(f"{extract_dir}/stops.json", 'w', 'utf8') as f:
            f.write(json.dumps(r.json(), sort_keys=True, ensure_ascii=False))
    except requests.exceptions.RequestException as e:
        print("[Requests error ]", e)
    
@task(log_prints=True, name="Query Wmata API for bus stops data", retries=3)
def load_to_bq()->None:
    os.system(f'bq load --source_format=CSV --clustering_fields=stop_sequence {project_id}:gtfs_static.stop_times {extract_dir}/stop_chunk_00 trip_id:NUMERIC,arrival_time:STRING,departure_time:STRING,stop_id:NUMERIC,stop_sequence:NUMERIC,stop_headsign:STRING,pickup_type:INTEGER,drop_off_type:INTEGER,shape_dist_traveled:FLOAT,timepoint:BOOLEAN')
    os.system(f'bq load --source_format=CSV --clustering_fields=stop_sequence {project_id}:gtfs_static.stop_times {extract_dir}/stop_chunk_01 trip_id:NUMERIC,arrival_time:STRING,departure_time:STRING,stop_id:NUMERIC,stop_sequence:NUMERIC,stop_headsign:STRING,pickup_type:INTEGER,drop_off_type:INTEGER,shape_dist_traveled:FLOAT,timepoint:BOOLEAN')

    os.system(f'bq load --source_format=CSV --skip_leading_rows=1 --clustering_fields=shape_pt_sequence {project_id}:gtfs_static.shapes {extract_dir}/shapes.txt shape_id:STRING,shape_pt_lat:FLOAT,shape_pt_lon:FLOAT,shape_pt_sequence:NUMERIC,shape_dist_traveled:FLOAT')
    os.system(f'bq load --source_format=CSV --skip_leading_rows=1 {project_id}:gtfs_static.stops {extract_dir}/stops.txt stop_id:NUMERIC,stop_code:INTEGER,stop_name:STRING,stop_desc:STRING,stop_lat:FLOAT,stop_lon:FLOAT,zone_id:NUMERIC,stop_url:STRING')

    os.system(f'bq load  --source_format=NEWLINE_DELIMITED_JSON --autodetect {project_id}:gtfs_static.json stops.json')


from prefect_dbt.cli.commands import DbtCoreOperation, DbtCliProfile
@task(name="dbt modelling")
def dbt_model():
    """Run dbt models"""

    dbt_path = Path(f"../wmata_bus/")
    
    dbt_cli_profile = DbtCliProfile.load("dbt-cli-profile")
    
    with DbtCoreOperation(
                    commands=["dbt debug"],
                    project_dir="/home/final/wmata_bus",
                    profiles_dir="/home/final/wmata_bus"
                    #,dbt_cli_profile = dbt_cli_profile # comment out if dbt asks for a dbt_cli_profile
        
    )as dbt_operation:
        result = dbt_operation.run()
        # do other things before waiting for completion
        
    return result


@flow(name="test")
def test_flow():
    unzip_file(query_gtfs_api())
    query_stops_json()
    load_to_bq()
    dbt_model()

if __name__ == '__main__':
    test_flow()