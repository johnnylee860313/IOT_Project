import RPi.GPIO as GPIO
import time

LOCK_GPIO = 23
PWM_FREQ = 50
STEP=15

GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_GPIO, GPIO.OUT)

pwm = GPIO.PWM(LOCK_GPIO, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def switch2deg(deg):
    dc = angle_to_duty_cycle(deg)
    pwm.ChangeDutyCycle(dc)

degrees = [45, 90, 135, 90]

sign = int(input('open or not ?'))

if sign == 1 :
    print("Door opened")
    for i in range(5):
        for deg in degrees:
            switch2deg(deg)
            time.sleep(0.5)
    pwm.stop()
    GPIO.cleanup()
else:
    pwm.stop()
    GPIO.cleanup()