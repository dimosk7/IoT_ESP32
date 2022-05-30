import  requests
import json
from datetime import datetime
import pymongo



## MongoDB

# creating MongoDB collection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["esp32"]
mycol = mydb["sensor_data"]

# retrieving data from Adafruit IO
r1 = requests.get("https://io.adafruit.com/api/v2/dimosk7/feeds/temper/data/chart")
r2 = requests.get("https://io.adafruit.com/api/v2/dimosk7/feeds/hum/data/chart")

# select data that should be inserted into MongoDB collection
temp = json.loads(r1.text)["data"]
hum = json.loads(r2.text)["data"]

# Option 1 : reading last line from a text file that contains the dates of the last added temp & hum values
with open("time_mongo.txt", "r") as f:
    last_time = f.readlines()[-1]

#Option 2: reading last record's date from MongoDB collection
mongo_dates = []
for x in mycol.find({}, {"date" : 1}).sort("date", -1):
    mongo_dates.append(x)

last_time = a[-1]["date"]

# find the position of the first row (date, temp, hum) we should insert into MongoDB collection (the other rows already exist)
cnt = 0
pos = 0
for i in temp :
    if i[0] > last_time :
        pos = cnt
        break
    cnt += 1

# storing the dates of temp and hum values in separate lists
date_temp = [x[0] for x in temp[pos:]]
date_hum = [x[0] for x in hum[pos:]]

# checking if dates are the same for both temp and hum values
dates = [0 if x in date_hum else x for x in date_temp]

# convert dates from str type to datetime type
date = [ datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ") for x in date_temp]

# storing temp and hum values in separate lists
val_temp = [float(x[1]) for x in temp[pos:]]
val_hum = [float(x[1]) for x in hum[pos:]]

# transforming the data into the appropriate form, so it can be inserted to MongoDB collection
mylist = list(zip(date, val_temp, val_hum))
list_data = [{"date" : x[0], "temperature" : x[1], "humidity" : x[2]} for x in mylist]


# insert multiple records into MongoDB collection
x = mycol.insert_many(list_data)