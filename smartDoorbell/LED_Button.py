import RPi.GPIO as GPIO
import time
BUTTON_PIN = 25
LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN,GPIO.OUT)

while True:
    BUTTON_STATUS = GPIO.input(BUTTON_PIN)
    if(BUTTON_STATUS == True):
        print("Button unpressed")
        GPIO.output(LED_PIN,0)
    else:
        print("Button pressed")
        GPIO.output(LED_PIN,1)
    time.sleep(0.5)
