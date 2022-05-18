import network
from machine import Pin
from umqtt.robust import MQTTClient
from time import time, sleep 
import time as TIME
import os 
import random
import sys
import dht
import machine


## global variables

boo = False

## define breadboard pins that are being used

pin_led = 4
pin_dht = 2
led = Pin(pin_led , Pin.OUT)
led.value(0)
d = dht.DHT11(machine.Pin(pin_dht))


## Functions

def check():
    client.check_msg()
    sleep(1)

def print_message(message):
    now = TIME.localtime(TIME.time())
    print("{}-{}-{} {}:{}:{} {}".format(now[0], now[1], now[2], now[3], now[4], now[5], message) )
    

def send_data() :
    global boo
    while boo == True :
        client.check_msg()
        try :
            start = time() 
            d.measure()
            temp = d.temperature()
            hum = d.humidity()
            client.publish(mqtt_feed_2,bytes(str(temp), 'utf-8'), qos=0)
            client.publish(mqtt_feed_3,bytes(str(hum), 'utf-8'), qos=0)
            print_message("Data sent to Adafruit successfully")
            while (boo == True) and (time() - start < 300) :
                check()
            
        except OSError :
            print_message("Data could not be sent")
        
 

        
## connect to WiFi

wlan = network.WLAN(network.STA_IF)
if not wlan.active():
        wlan.active(True)

while not wlan.isconnected():
    try :
        wlan.connect("VODAFONE_****", "8e**********")
    except OSError :
        print_message("Could not connect to WiFi. Wait...")
    sleep(1)   
print_message("Connected to WiFi")
a = wlan.ifconfig()
sleep(1)
print_message("The IP-level network interface parameters are :\n\n\tESP32 IP address: {} \n\tSubnet mask: {} \n\tGateway: {} \n\tDNS: {}\n".format(a[0],a[1],a[2],a[3]))




## connect to MQTT broker (Adafruit)

adaf_url = "io.adafruit.com"
adaf_user = "dimosk7"
adaf_key = "aio_WbhA302FG2VkACrhMR9S8cgD3TKf"


#define Adafruit feeds
adaf_feed = "led-1"
adaf_temp = "temper"
adaf_message = "message"
adaf_hum = "hum"
mqtt_feed = bytes(("{:s}/feeds/{:s}".format(adaf_user, adaf_feed)), "utf-8")
mqtt_feed_2 = bytes(("{:s}/feeds/{:s}".format(adaf_user, adaf_temp)), "utf-8")
mqtt_feed_3 = bytes(("{:s}/feeds/{:s}".format(adaf_user, adaf_hum)), "utf-8")
mqtt_feed_4 = bytes(("{:s}/feeds/{:s}".format(adaf_user, adaf_message)), "utf-8")


#create random id for MQTT broker connection
random_num = int.from_bytes(os.urandom(2), 'little')
mqtt_id = str(random_num)

client = MQTTClient( client_id = mqtt_id,
                     server = adaf_url,
                     user = adaf_user,
                     password = adaf_key,
                     ssl = False)

client.connect()


#define callback function that runs when we send data from ADafruit to ESP32
def call_back_routine(feed, msg):
    global boo
    if adaf_feed in feed :
        if str(msg, "utf-8") == "ON":
            led.value(1)
            boo = True
            send_data()
        else :
            led.value(0)
            boo = False
            print_message("Stopped sending data")
            
                  
client.set_callback(call_back_routine)
client.subscribe(mqtt_feed)


## running when led is "OFF"

while True :
    client.check_msg()
    sleep(0.5)
