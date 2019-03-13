import matplotlib.pyplot as plt
import matplotlib
import datetime

from pymongo import MongoClient

client = MongoClient('142.150.208.202', 27017)
db = client.create
collection = db.hi

if __name__ == '__main__':
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    indexes_1 = ['Montreal', 'Sydney', 'Toronto', 'New york', 'Jakarta']
    indexes_2 = ['Shanghai', 'Tehran', 'London', 'Seoul', 'Tokyo']

    for index in indexes_1:
        data = list(collection.find({'data.city': index}))[5:29]
        times = [datetime.datetime.strftime(datetime.datetime.strptime(value['date_time'], '%Y-%m-%d %H:%M:%S.%f'), '%H:%M') for value in data]
        hi = [value['data']['hi'] for value in data]
        ax1.plot(times, hi, 'o', label=index)

    for index in indexes_2:
        data = list(collection.find({'data.city': index}))[5:29]
        times = [datetime.datetime.strftime(datetime.datetime.strptime(value['date_time'], '%Y-%m-%d %H:%M:%S.%f'), '%H:%M') for value in data]
        hi = [value['data']['hi'] for value in data]
        ax2.plot(times, hi, 'o', label=index)
    ax1.legend()
    ax1.set_title('Heat Index in 24 hours')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Heat Index')
    ax2.legend()
    ax2.set_title('Heat Index in 24 hours')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Heat Index')

    plt.show()
    
