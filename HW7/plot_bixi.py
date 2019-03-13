import matplotlib.pyplot as plt
import matplotlib
import datetime

from pymongo import MongoClient

client = MongoClient('142.150.208.202', 27017)
db = client.create
collection = db.bikes

def calculate_load(bikes):
    bikes_in_use = 0
    total_bikes = 0
    for bike in bikes:
        bikes_in_use += bike['bikes']
        total_bikes += bike['station_capacity']

    print(bikes_in_use, total_bikes)
    return bikes_in_use / total_bikes

if __name__ == '__main__':
    fig, ax = plt.subplots()
    bikes = list(collection.find({}))[0:24]
    times = [datetime.datetime.strftime(datetime.datetime.strptime(value['date_time'], '%Y-%m-%d %H:%M:%S.%f'), '%H:%M') for value in bikes]
    load = [calculate_load(value['data']) for value in bikes]
    ax.plot(times, load, 'o', label='Bicycle Load')
    ax.legend()
    ax.set_title('Bicycle load as a function of time')
    ax.set_xlabel('Time')
    plt.show()
    
