import matplotlib.pyplot as plt
import matplotlib
import datetime
import pymongo

from pymongo import MongoClient

client = MongoClient('142.150.208.202', 27017)
db = client.create
collection = db.aqi

if __name__ == '__main__':
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    indexes_1 = ['Montreal', 'Rozelle Sydney East, Australia', 'Toronto', 'New York', 'Shanghai (上海)']
    indexes_2 = ['Tehran Imam Khomeini, Iran', 'London', 'Seoul (서울)', 'Jakarta Central (US Consulate), Indonesia', 'Meguro (目黒)']

    for index in indexes_2:
        data = list(collection.find({'data.city': index}).sort('date_time', pymongo.ASCENDING))[38:61]
        times = [datetime.datetime.strftime(datetime.datetime.strptime(value['date_time'], '%Y-%m-%d %H:%M:%S.%f'), '%H:00') for value in data]
        hi = [value['data']['aqi'] for value in data]
        ax1.plot(sorted(times), hi, 'o', label=index)

    # for index in indexes_2:
    #     data = list(collection.find({'data.city': index}).sort('date_time', pymongo.ASCENDING))[38:61]
    #     times = [datetime.datetime.strftime(datetime.datetime.strptime(value['date_time'], '%Y-%m-%d %H:%M:%S.%f'), '%H:%M') for value in data]
    #     hi = [value['data']['aqi'] for value in data]
    #     ax2.plot(times, hi, 'o', label=index)
    ax1.legend()
    ax1.set_title('AQI in 24 hours')
    ax1.set_yticks([i * 8 for i in range(25)])
    ax1.set_yticklabels([i * 8 for i in range(25)])
    # ax2.set_yticks([i * 8 for i in range(25)])
    # ax2.set_yticklabels([i * 8 for i in range(25)])

    ax1.set_xlabel('Time')
    ax1.set_ylabel('AQI')
    # ax2.set_title('AQI in 24 hours')
    # ax2.set_xlabel('Time')
    # ax2.set_ylabel('AQI')
    # ax2.legend()

    plt.show()
    
