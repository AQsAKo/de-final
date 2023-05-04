#!/usr/bin/env python

import os
import argparse

from time import time

import requests
import codecs
import json
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson

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
        feed = gtfs_realtime_pb2.FeedMessage()
        r = requests.get('https://api.wmata.com/gtfs/bus-gtfsrt-tripupdates.pb', headers = headers)
        print(r.status_code)
        feed.ParseFromString(r.content)
        #print(feed)
        with codecs.open(f"{extract_dir}/trip_updates.json", 'w', 'utf8') as f:
            #f.write(json.dumps(MessageToJson(feed, indent=2), sort_keys=True, ensure_ascii=False))
            f.write(json.dumps(r.json(), sort_keys=True, ensure_ascii=False))

    except Exception as e:
        print("[Error {0}]".format(e.strerror))

if __name__ == '__main__':
    # Parse the command line arguments and calls the main program
    parser = argparse.ArgumentParser(description='Ingest bus stops data to local|cloud datalake')

    parser.add_argument('--api_key', help='wmata api key')
    parser.add_argument('--extract_dir', help='target directory for gtfs static data')

    args = parser.parse_args()

    main(args)