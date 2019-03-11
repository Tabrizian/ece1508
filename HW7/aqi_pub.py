import requests
import json
import datetime
import time
import paho.mqtt.client as mqtt

from datetime import timedelta

AQI_API_TOKEN = '6972c6d7f83e0702d37c98e9fa94f65c2b419541'
AQI_API_URL = 'http://api.waqi.info/feed/'
BROKER_ADDRESS = '142.150.208.252'
BROKER_PORT = 1883
STUDENT_NUMBER = '1005167454'


cities = ['Montreal', 'Sydney', 'Toronto', 'Newyork',
        'Shanghai', 'Tehran', 'London', 'Seoul',
        'Jakarta', 'Tokyo']


def get_air_quality(city):
    url = AQI_API_URL + city.lower() + '/?token=' + AQI_API_TOKEN
    response = requests.get(url)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8'))['data']
        trimmed_data = {
                'date_time': str(datetime.datetime.utcnow()),
                'data': {}
        }
        trimmed_object = {}
        trimmed_object['aqi'] = response['aqi']
        trimmed_object['city'] = response['city']['name']
        trimmed_object['iaqi'] = response['iaqi']
        trimmed_object['time'] = response['time']

        trimmed_data['data'] = trimmed_object

        return trimmed_data
    else:
        return None



def fetch_and_publish():
    for city in cities:
        city_data = get_air_quality(city)
        topic = 'ece1508/%s/%s/aqi' % (STUDENT_NUMBER, city.lower())
        client.publish(topic, json.dumps(city_data))
        print('Published %s city to %s topic' % (city, topic))

if __name__ == '__main__':


    while True:
        client = mqtt.Client()
        client.connect(BROKER_ADDRESS, BROKER_PORT)
        client.loop_start()

        fetch_and_publish()
        client.disconnect()
        dt = datetime.datetime.now() + timedelta(hours=1)
        while datetime.datetime.now() < dt:
            time.sleep(2)


