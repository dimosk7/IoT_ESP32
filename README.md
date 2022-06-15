# IoT_ESP32

## Overview

This IoT project has two stages. In the first phase , an ESP-32 microcontroller is used to send IoT data (temperature and relative humidity data) to Adafruit IO MQTT Broker using MQTT protocol. The next phase is where the raw data is retrieved from Adafruit IO and after processing, it is then strored in a MySQL database, a MongoDB database or a CSV file. If desirable,the data can be visualized on PowerBI. The first stage is executed by the programm (Micropython code) that has been uploaded to ESP-32, whereas the second is running on user's computer (pyton code).

## How it works

First, a temperature and humidity sensor (DHT sensor) is wired to ESP-32. The microcontroller's main function is to read sensor's values every 5 minutes and send it to Adafruit IO. This process is controlled by a toggle displayed on our Adafruit dashboard. More analytically, the process starts when the toggle is switched to "ON" function, whereas the process stops running when the toggle is switched back to "ΟFF" state. To indicate system's state, a LED has been connected to ESP-32 (lights up when "ON").

* Thonny IDE is used to write and upload code to ESP-32



References :
Notes from Internet of Things online course - Robotonio
