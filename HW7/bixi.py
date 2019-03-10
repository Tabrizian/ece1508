import requests
import json
import datetime
import time

from datetime import timedelta
from pymongo import MongoClient


BIXI_DATA_URL = 'http://portal.cvst.ca/api/0.1/bixi'
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.create
collection = db.bikes

def store_in_db(document):
    collection.insert_one(document)

def get_bixi_data():
    response = requests.get(BIXI_DATA_URL)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8'))
        trimmed_data = {
                'date_time': str(datetime.datetime.utcnow()),
                'data': []
        }
        response = response[0:30]
        for item in response:
            trimmed_object = {}
            trimmed_object['bikes'] = item['bikes']
            trimmed_object['empty_docks'] = item['empty_docks']
            trimmed_object['station_capacity'] = item['bikes'] + item['empty_docks']
            trimmed_object['station_id'] = item['id']
            trimmed_object['date_time'] = item['date_time']
            trimmed_data['data'].append(trimmed_object)

        return trimmed_data
    else:
        return None

def fetch_and_store():
    bixi_data = get_bixi_data()
    store_in_db(bixi_data)
    print('Stored new data at %s' % str(datetime.datetime.now()))



if __name__ == "__main__":
    while True:
        fetch_and_store()
        dt = datetime.datetime.now() + timedelta(hours=1)
        while datetime.datetime.now() < dt:
            time.sleep(2)




