import requests
import json
import datetime
import time

from datetime import timedelta
from pymongo import MongoClient


TRAFFIC_DATA_URL = 'http://portal.cvst.ca/api/0.1/HW_speed'
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.create
collection = db.traffic

def store_in_db(document):
    collection.insert_one(document)

def get_traffic_data():
    response = requests.get(TRAFFIC_DATA_URL)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8'))[0]['data']
        trimmed_data = {
                'date_time': str(datetime.datetime.utcnow()),
                'data': []
        }
        for item in response:
            trimmed_object = {}
            trimmed_object['avg_speed_capped'] = item['avg_speed_capped']
            trimmed_object['free_flow_speed'] = item['free_flow_speed']
            trimmed_object['road_name'] = item['main_road_name'] + '/' + item['ref_road_name']
            trimmed_data['data'].append(trimmed_object)

        return trimmed_data
    else:
        return None

def fetch_and_store():
    traffic_data = get_traffic_data()
    store_in_db(traffic_data)
    print('Stored new data at %s' % str(datetime.datetime.now()))



if __name__ == "__main__":
    while True:
        fetch_and_store()
        dt = datetime.datetime.now() + timedelta(hours=1)
        while datetime.datetime.now() < dt:
            time.sleep(2)




