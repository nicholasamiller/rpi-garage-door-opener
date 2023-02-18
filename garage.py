import RPi.GPIO as  GPIO
import time
import logging

logging.basicConfig(filename='garageDoor.log', level=logging.DEBUG)

CHANNEL=21



def logPinState():
    logging.info(f"GPIO pin {CHANNEL} currently set to  {GPIO.input(CHANNEL)}.")

def triggerGarage():
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(CHANNEL, GPIO.OUT) 
    logging.info("Garage door triggered")
    logPinState()
    GPIO.output(CHANNEL, GPIO.HIGH)
    logPinState()
    time.sleep(1)
    GPIO.output(CHANNEL, GPIO.LOW)
    time.sleep(1)
    logPinState()
    GPIO.cleanup()


