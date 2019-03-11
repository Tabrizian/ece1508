import requests
import json
import datetime
import time
import paho.mqtt.client as mqtt

from datetime import timedelta

OWN_API_TOKEN = 'fb555e4f72c44f8e10255bab02c556bb'
OWN_API_URL = 'https://api.openweathermap.org/data/2.5/weather?q='
BROKER_ADDRESS = '142.150.208.252'
BROKER_PORT = 1883
STUDENT_NUMBER = '1005167454'


cities = ['Montreal', 'Sydney', 'Toronto', 'New york',
        'Shanghai', 'Tehran', 'London', 'Seoul',
        'Jakarta', 'Tokyo']


def get_weather(city):
    url = OWN_API_URL + city.lower() + '&appid=' + OWN_API_TOKEN
    response = requests.get(url)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8'))
        trimmed_data = {
                'date_time': str(datetime.datetime.utcnow()),
                'data': {}
        }
        T = response['main']['temp'] - 273.15
        R = response['main']['humidity'] / 100.00
        C1 = -0.878469475556
        C2 = 1.61139411
        C3 = 2.33854883889
        C4 = -0.14611605
        C5 = -0.012308094
        C6 = -0.0164248277778
        C7 = 0.002211732
        C8 = 0.00072546
        C9 = -0.000003582
        hi = C1 + C2 * T + C3 * R + C4 * T * R + C5 * T * T \
             + C6 * R * R + C7 * T * T * R + C8 * T * R * R + C9 * T * T * R * R

        trimmed_object = {}
        trimmed_object['hi'] = hi
        trimmed_object['city'] = response['name']
        trimmed_data['data'] = trimmed_object

        return trimmed_data
    else:
        return None



def fetch_and_publish():
    for city in cities:
        city_data = get_weather(city)
        topic = 'ece1508/%s/%s/hi' % (STUDENT_NUMBER, city.lower())
        client.publish(topic, json.dumps(city_data))
        print('Published %s city to %s topic' % (city, topic))

if __name__ == '__main__':


    while True:
        client = mqtt.Client()
        client.connect(BROKER_ADDRESS, BROKER_PORT)
        client.loop_start()

        fetch_and_publish()
        dt = datetime.datetime.now() + timedelta(hours=1)
        while datetime.datetime.now() < dt:
            time.sleep(2)


