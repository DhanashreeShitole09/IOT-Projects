
### AUTOMOTIVE VECHILE

import RPi.GPIO as GPIO
import time
import Buzzer
from time import sleep


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_LED = 2
buzzer = 17
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(2,GPIO.OUT) #for led
GPIO.setup(buzzer,GPIO.OUT)

def distance():

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back

    distance = (TimeElapsed * 34300) / 2
 
    return distance
def buzzer():
    
    if dist<11:
        GPIO   
       

 
if __name__ == '__main__':
    try:
        while True:
            
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist < 11:
                GPIO.output(2,True)
                GPIO.output(17,GPIO.HIGH)
                print("LED ON")
                    
            else:
                GPIO.output(2,False)
                GPIO.output(17,GPIO.LOW)
                print("LED OFF")
                
                #buzzer.LOW
                time.sleep(5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
if dist<11:
    GPIO.output(17,GPIO.HIGH)
    time.sleep(1)
else:
    GPIO.output(17,GPIO.LOW)
    time.sleep(1)    
    
    
while True:
    buzzer.beep()    
