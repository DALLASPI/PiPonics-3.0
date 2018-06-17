import RPi.GPIO as GPIO
import time

##GPIO SETUP
channel = 36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print ("water detected")
    else:
        print("no water detected")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
        time.sleep(1)
               
