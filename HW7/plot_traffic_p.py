import matplotlib.pyplot as plt
import matplotlib
import datetime

from pymongo import MongoClient

client = MongoClient('142.150.208.202', 27017)
db = client.create
collection = db.traffic

if __name__ == '__main__':
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    traffic = list(collection.find({}))[0:24]
    times = [datetime.datetime.strftime(datetime.datetime.strptime(value['date_time'], '%Y-%m-%d %H:%M:%S.%f'), '%H:%M') for value in traffic]

    indexes_1 = [0, 1, 3, 4, 5]
    indexes_2 = [6, 22, 23, 60, 65]

    for index in indexes_1:
        avg_traffic = [value['data'][index]['avg_speed_capped'] / value['data'][index]['free_flow_speed'] for value in traffic]
        ax1.plot(times, avg_traffic, 'o', label=traffic[0]['data'][index]['road_name'])
    for index in indexes_2:
        avg_traffic = [value['data'][index]['avg_speed_capped'] / value['data'][index]['free_flow_speed'] for value in traffic]
        ax2.plot(times, avg_traffic, 'o', label=traffic[0]['data'][index]['road_name'])
    ax2.legend()
    ax1.legend()
    ax2.set_title('Average Speed Capped in 24 hours')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Average Speed Capped')
    ax1.set_title('Average Speed Capped in 24 hours')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Average Speed Capped')

    plt.show()
    
