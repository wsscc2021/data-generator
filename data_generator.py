"""
    This project generate data-set that is used subway in/out for data analytics.
    1. It is based on Daejeon subway 1st line.
        - Daejeon subway line
        - 2020-01-01 ~ 2020-12-31
        - Passenger info
            - age
            - gender
        - in/out info
            - in station and out station per passenger
            - datetime
    2. It store in subway_record.csv file
"""
# Module import
import random
import datetime
import time
import csv

# Subway stations(Daejeon subway 1st line)
stations = [
    'Banseok', 'Jijok', 'Noeun', 'World_cup_stadium', 'National_cemetery', 'Guam',
    'Yuseong_spa', 'Gapcheon', 'Wolpyeong', 'Galma', 'Goverment_complex_daejeon', 
    'City_hall', 'Tanbang', 'Yongmun', 'Oryong', 'Seodaejeon_negeori', 'Junggu_office',
    'Jungangro', 'Daejeon', 'Daedong', 'Sinheung', 'Panam'
]

# Pricing class based on passenger's age
def class_generate(passenger_age):
    if passenger_age < 20:
        return 'youth'
    elif passenger_age < 25:
        return 'college_student'
    elif passenger_age < 60:
        return 'adult'
    elif passenger_age < 80:
        return 'senior_citizen'
    else:
        return False

# Pricing based on passenger's class(It based on age)
def price_generate(passenger_class):
    return {
        'youth': 800,
        'college_student': 1000,
        'adult': 1200,
        'senior_citizen': 800
    }.get(passenger_class, False)

# In-station is generated by random.
# Last-station can't be In-station, and that consider direction.
def ride_station_generate(direction):
    if direction == stations[0]:
        return random.choice(stations[1:])
    elif direction == stations[-1]:
        return random.choice(stations[:-1])
    else:
        return False

# Out-station is generated by random.
# If passenger arrived Last-station, must be take off subway.
#   - Random range: In-station + 1 ~ Last-station
# Of course, It consider direction.
def quit_station_generate(direction, ride_station):
    if direction == stations[0]:
        max_move_station_count = stations.index(ride_station) + 1
        move_station_count = random.randrange(1,max_move_station_count)
        return stations[stations.index(ride_station) - move_station_count]
    elif direction == stations[-1]:
        max_move_station_count = len(stations) - stations.index(ride_station)
        move_station_count = random.randrange(1,max_move_station_count)
        return stations[stations.index(ride_station) + move_station_count]
    else:
        return False

# Station-in-datetime is generated by random.
#   - Random range: 2020-01-01 ~ 2020-12-31
def ride_datetime_generate(random_time_range_start, random_time_range_end):
    return datetime.datetime(2020,1,1,0,0,0) \
           + datetime.timedelta(days=random.randrange(365)) \
           + datetime.timedelta(seconds=random.randrange(random_time_range_start, random_time_range_end))

# Station-out-datetime is generated by moved station count from Station-in-datetime.
# It takes 3 minutes to move one station.
def quit_datetime_generate(ride_station, quit_station, ride_datetime):
    minutes = abs(stations.index(ride_station) - stations.index(quit_station)) * 3
    return ride_datetime + datetime.timedelta(minutes=minutes)    

# Main function
# It generate raw data-set.
# 1. Mostly passenger use the subway at 7-9 or 17-19 time. (get-work and get-home time)
# 2. Mostly passenger is 10-50 years-old.
def random_data_generate(csvfile_writer):
    terms = {
        'wholeday': [0,86400], #하루종일
        'get_work': [25200,32400], #7시~9시
        'get_home': [61200,68400], #17시~19시
    }
    for term, timerange in terms.items():
        for _x in range(1,5000000):
            passenger_gender = random.choice(['male','female'])
            passenger_age    = random.randrange(13,80) if term == 'wholeday' else random.randrange(13,50)
            passenger_class  = class_generate(passenger_age)
            passenger_price  = price_generate(passenger_class)
            direction        = random.choice([stations[0],stations[-1]])
            ride_station     = ride_station_generate(direction)
            ride_datetime    = ride_datetime_generate(timerange[0],timerange[1])
            quit_station     = quit_station_generate(direction, ride_station)
            quit_datetime    = quit_datetime_generate(ride_station, quit_station, ride_datetime)
            csvfile_row_write(
                csvfile_writer, passenger_gender, passenger_age, passenger_class, passenger_price,
                direction, ride_station, ride_datetime, quit_station, quit_datetime)

# Write to csv file.
def csvfile_row_write(csvfile_writer, passenger_gender, passenger_age, passenger_class, passenger_price, 
                      direction, ride_station, ride_datetime, quit_station, quit_datetime):
    for action in [ "in", "out" ]:
        passenger_price = passenger_price if action == "in" else 0
        csvfile_writer.writerow([
            ride_station,
            direction,
            action,
            passenger_gender,
            passenger_age,
            passenger_class,
            passenger_price,
            ride_datetime,
            ride_datetime.strftime("%Y"),
            ride_datetime.strftime("%m"),
            ride_datetime.strftime("%d"),
            ride_datetime.strftime("%H")
        ])

if __name__ == '__main__':
    csvfile = open('subway_record.csv','a',newline='')
    csvfile_writer = csv.writer(csvfile)
    csvfile_writer.writerow([
        "station", "direction", "in_out", "passenger_gender", "passenger_age", "passenger_class",
        "passenger_price", "datetime", "year", "month", "day", "hour"])
    random_data_generate(csvfile_writer)
    csvfile.close()