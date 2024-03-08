### SMART HOME AUTOMATION 2


import RPi.GPIO as GPIO
import time

from picamera import PiCamera
camera = PiCamera()

import Adafruit_DHT
from Adafruit_IO import Client

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

DHT_DATA_PIN = 22 #DHT11 sensor

GPIO.setup(11,GPIO.IN) #IR Sensor at door

GPIO.setup(12,GPIO.OUT) #Person detect

GPIO.setup(8,GPIO.OUT) #Buzzer

GPIO.setup(5,GPIO.IN) #MQ2 sensor

GPIO.setup(15,GPIO.OUT) #LED for exaust
GPIO.setup(16,GPIO.OUT) #LED for Window

GPIO.setup(18,GPIO.OUT) #for fan control
GPIO.setup(19,GPIO.OUT)

pwm= GPIO.PWM(18,100) #for fan control
pwm.start(100)

ADAFRUIT_IO_USERNAME = "Dhanashree_99"
ADAFRUIT_IO_KEY = "aio_ePlr19rmVFbEcz0atSDYBMenBDa1"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

slider_feed = aio.feeds('slider') # fan connected to Pin 21
distance_feed1 = aio.feeds('light') # Home light at pin 19

temperature_feed = aio.feeds('temp')
humidity_feed = aio.feeds('humidity')
dht22_sensor = Adafruit_DHT.DHT11

while 1:
value=GPIO.input(5) #MQ2
print(value)

if(value==0):
GPIO.output(8,True)
print("Buzzer Is ON")
GPIO.output(15,True)
GPIO.output(16,True)
time.sleep(1)

if(value==1): #mQ2
GPIO.output(8,False)
GPIO.output(15,False)
GPIO.output(16,False)
print("Buzzer Is Off")
time.sleep(0.1)

if(GPIO.input(11)==True): #person detected at door
GPIO.output(12,True)
for i in range (0,100)

camera.capture("/home/pi/Pictures/img"i".jpg") # image name
print("Person Captured")
print("LED ON")
else:
GPIO.output(12,False)
time.sleep(0.1)

#ADA fruit Cloud
print("Receiving data..")
status = aio.receive(slider_feed.key).value #FAN control
print(status)

pwm.ChangeDutyCycle(int(status))
time.sleep(0.01)
status1 = aio.receive(distance_feed1.key).value
print(status1)

if status1 == "ON":
GPIO.output(19,True) #home light control
print("LED ON")
time.sleep(0.01)
else:
GPIO.output(19,False)
print("LED OFF")
time.sleep(0.01)
humidity, temperature = Adafruit_DHT.read_retry(dht22_sensor, DHT_DATA_PIN)

if humidity is not None and temperature is not None:
print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
temperature = '%.2f'%(temperature)
humidity = '%.2f'%(humidity)
aio.send(temperature_feed.key, str(temperature))
aio.send(humidity_feed.key, str(humidity))
else:
print('Failed to get DHT22 Reading, trying again in ', DHT_READ_TIMEOUT, 'seconds')
time.sleep(5)
pwm.stop()
GPIO.cleanup