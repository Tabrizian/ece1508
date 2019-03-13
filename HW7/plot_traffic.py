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

    avg_traffic = [value['data'][0]['avg_speed_capped'] for value in traffic]
    ax1.plot(times, avg_traffic, 'o', label=traffic[0]['data'][0]['road_name'])
    avg_traffic = [value['data'][1]['avg_speed_capped'] for value in traffic]
    ax1.plot(times, avg_traffic, 'o', label=traffic[0]['data'][1]['road_name'])
    avg_traffic = [value['data'][3]['avg_speed_capped'] for value in traffic]
    ax1.plot(times, avg_traffic, 'o', label=traffic[0]['data'][3]['road_name'])
    avg_traffic = [value['data'][4]['avg_speed_capped'] for value in traffic]
    ax1.plot(times, avg_traffic, 'o', label=traffic[0]['data'][4]['road_name'])
    avg_traffic = [value['data'][5]['avg_speed_capped'] for value in traffic]
    ax1.plot(times, avg_traffic, 'o', label=traffic[0]['data'][5]['road_name'])
    avg_traffic = [value['data'][6]['avg_speed_capped'] for value in traffic]
    ax2.plot(times, avg_traffic, 'o', label=traffic[0]['data'][6]['road_name'])
    avg_traffic = [value['data'][22]['avg_speed_capped'] for value in traffic]
    ax2.plot(times, avg_traffic, 'o', label=traffic[0]['data'][22]['road_name'])
    avg_traffic = [value['data'][23]['avg_speed_capped'] for value in traffic]
    ax2.plot(times, avg_traffic, 'o', label=traffic[0]['data'][23]['road_name'])
    avg_traffic = [value['data'][60]['avg_speed_capped'] for value in traffic]
    ax2.plot(times, avg_traffic, 'o', label=traffic[0]['data'][60]['road_name'])
    avg_traffic = [value['data'][65]['avg_speed_capped'] for value in traffic]
    ax2.plot(times, avg_traffic, 'o', label=traffic[0]['data'][65]['road_name'])
    ax2.legend()
    ax1.legend()
    ax2.set_title('Average Speed Capped in 24 hours')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Average Speed Capped')
    ax1.set_title('Average Speed Capped in 24 hours')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Average Speed Capped')

    plt.show()
    
