
# coding: utf-8

# In[ ]:


import serial
import io
import thingspeak
import requests
import time


# In[ ]:


ser = serial.Serial('/dev/cu.usbmodem1411', baudrate=19200, timeout=1)
#Sean's Macbook can be usbmoden1411 or 1412 | Will need to change when we transfer to raspberry pi


# In[ ]:


def _readline(ser):
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)


# In[ ]:


def remove(line_byte):
    ser.write(line_byte)
    init=str(_readline(ser))
    for ch in [
        " ",
        "b'=4",
        "b'=1",
        "b'=2",
        "20\\r'",
        "m/s",
        "\\xb0",
        "Windrichtung",
        "Windgeschwindigkeit",
        "Temperatur",
        "C",
        "rel.Feuchte",
        "%",
        "SMP10-VStrahlung",
        "W/m2",
        "PQS1Strahlung",
        "\\xb5mol",
        "Wassergehalt",
        "Bodentemperatur"
    ]:
        if ch in init:
            init=init.replace(ch,"")
    return init


# In[ ]:


def post_data():
    
    wind_speed=remove(b'$01B01\r')
    wind_direction=remove(b'$01B02\r')
    temperature=remove(b'$01B03\r')
    humidity=remove(b'$01B04\r')
    irradiation1=remove(b'$01B05\r')
    irradiation2=remove(b'$01B06\r')
    air_pressure=remove(b'$01B011\r')
    precipitation=remove(b'$01B012\r')
    requests.get('https://api.thingspeak.com/update?api_key=9ZE7XDYROU8LRKOV&field1=' + str(wind_speed) 
                 + '&field2=' + str(wind_direction)
                 + '&field3=' + str(humidity)
                 + '&field4=' + str(irradiation1)
                 + '&field5=' + str(irradiation2)
                 + '&field6=' + str(temperature)
                 + '&field7=' + str(air_pressure)
                 + '&field8=' + str(precipitation))


# In[ ]:


def executeSomething():
    post_data()
    time.sleep(60)

while True:
    executeSomething()

