import  requests
import json
import mysql.connector
import csv
##testing

## get data from Adafruit feeds

r = requests.get("https://io.adafruit.com/api/v2/dimosk7/feeds/temper/data/chart")
r1 = requests.get("https://io.adafruit.com/api/v2/dimosk7/feeds/hum/data/chart")

temp = json.loads(str(r.content, "utf-8"))
hum = json.loads(str(r1.content, "utf-8"))

adaf_data = temp["data"]
adaf_hum = hum["data"]

##put all data to one list

j = 0
for i in adaf_hum:
    adaf_data[j].append(i[1])
    j+=1

    
## Export data to Excel

def replace_z(n):
    return n.replace("Z","")


#columns names
header = [ "date", "time","temperature", "humidity"]


# create a list with values that do not already exist in the csv file
# to update the csv file without creating duplicates, we write the datetime of the last value to a text file.

csv_data = []

with open("time_excel.txt", "r") as f:
    boo = f.read()
if boo == "" :
    for i in adaf_data:
        a = i[0].split("T")
        b = list(map(replace_z, a))
        b.append(int(i[1].replace(".0","")))
        b.append(int(i[2].replace(".0","")))
        csv_data.append(b)
    with open("time_excel.txt", "w") as f:
        f.write(adaf_data[-1][0])
    with open('sensor.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
else:
    with open("time_excel.txt", "r") as f:
        last_time = f.readlines()[-1]
        for i in adaf_data:
            if i[0] > last_time : # we add values whose datatime are bigger than the one that we read in text's last line.
                print(i[1])
                a = i[0].split("T")
                b = list(map(replace_z, a))
                b.append(int(i[1].replace(".0", "")))
                b.append(int(i[2].replace(".0", "")))
                csv_data.append(b)
        if bool(csv_data):
            with open("time_excel.txt", "a") as f:
                f.write("\n")
                f.write(adaf_data[-1][0])


# write values to csv file

with open('sensor.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)



## Export data to MySQL database

sql_data = []

with open("time_sql.txt", "r") as f:
    boo = f.read()
if boo == "" :
    for i in adaf_data:
        a = i[0].split("T")
        b = list(map(replace_z, a))
        b.append(int(i[1].replace(".0","")))
        b.append(int(i[2].replace(".0","")))
        sql_data.append(b)
    with open("time_sql.txt", "w") as f:
        f.write(adaf_data[-1][0])
else:
    with open("time_sql.txt", "r") as f:
        last_time = f.readlines()[-1]
        for i in adaf_data:
            if i[0] > last_time :
                a = i[0].split("T")
                b = list(map(replace_z, a))
                b.append(int(i[1].replace(".0", "")))
                b.append(int(i[2].replace(".0", "")))
                sql_data.append(b)
        if bool(sql_data):
            with open("time_sql.txt", "a") as f:
                f.write("\n")
                f.write(adaf_data[-1][0])


# connect to MySQL

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="dimosk",
  database="esp32",
  auth_plugin="mysql_native_password"
)


# store data to MySql database

mycursor = mydb.cursor()

for i in sql_data:
    sql = "INSERT INTO sensor_data (date,time,temperature,humidity) VALUES (%s,%s,%s,%s)"
    val = (i[0], i[1], i[2], i[3])
    mycursor.execute(sql, val)

mydb.commit()

###testing new branches


