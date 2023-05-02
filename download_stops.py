#!/usr/bin/env python

import os
import argparse

from time import time

import requests
import codecs
import json

def main(main_params):

    api_key = main_params.api_key
    extract_dir = main_params.extract_dir

    headers = {
        # Request headers
        'api_key': api_key,
    }

    #params = urllib.parse.urlencode({})

    try:
        #print(f'{extract_dir}')
        r = requests.get('https://api.wmata.com/Bus.svc/json/jStops', headers = headers)
        print(r.status_code)
        #conn = http.client.HTTPSConnection('api.wmata.com')
        #conn.request("GET", "/gtfs/bus-gtfs-static.zip?%s" % params, "{body}", headers)
        #response = conn.getresponse()
        #data = response.read()
        with codecs.open(f"{extract_dir}/stops.json", 'w', 'utf8') as f:
            f.write(json.dumps(r.json(), sort_keys=True, ensure_ascii=False))
        #with zipfile.ZipFile(io.BytesIO(r.content),"r") as zip_ref:
        #    zip_ref.extractall(extract_dir)
        #conn.close()

    except Exception as e:
        print("[Error {0}]".format(e.strerror))

if __name__ == '__main__':
    # Parse the command line arguments and calls the main program
    parser = argparse.ArgumentParser(description='Ingest bus stops data to local|cloud datalake')

    parser.add_argument('--api_key', help='wmata api key')
    parser.add_argument('--extract_dir', help='target directory for gtfs static data')

    args = parser.parse_args()

    main(args)