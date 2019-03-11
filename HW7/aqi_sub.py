import requests
import json
import datetime
import time
import paho.mqtt.client as mqtt

from pymongo import MongoClient

BROKER_ADDRESS = '142.150.208.252'
BROKER_PORT = 1883
STUDENT_NUMBER = '1005167454'
cities = ['Montreal', 'Sydney', 'Toronto', 'Newyork',
        'Shanghai', 'Tehran', 'London', 'Seoul',
        'Jakarta', 'Tokyo']

client = MongoClient('localhost', 27017)
db = client.create
collection = db.aqi

def on_connect(client, userdata, flags, rc):
    for city in cities:
        topic = 'ece1508/%s/%s/aqi' % (STUDENT_NUMBER, city.lower())
        client.subscribe(topic)

def on_message(client, userdata, message):
    data = json.loads(str(message.payload, encoding='utf-8'))
    collection.insert_one(data)
    print('Saved city %s at %s' % (data['data']['city'], str(datetime.datetime.now())))


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, BROKER_PORT)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
