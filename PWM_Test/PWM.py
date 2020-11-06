import RPi.GPIO as GPIO
import time, sys

LED = 19
SW1 = 17 # Brightness up
SW2 = 18 # Brightness down
SW3 = 27 # LED on/off

brightness = 50
flag = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwm = GPIO.PWM(LED, 50)

def pressSwitch(key):
    global pwm, flag, brightness
    flag = not flag
    if flag:
        brightness = 50
        pwm.start(brightness)
        print("\nLight on")
    else:
        pwm.stop()
        brightness = 50
        print("\nLight off")

def pressUp():
    global pwm, brightness
    brightness = brightness + 1
    if brightness > 100:
        brightness = 100
    pwm.ChangeDutyCycle(brightness)

def pressDown():
    global pwm, brightness
    brightness = brightness - 1
    if brightness < 0:
        brightness = 0
    pwm.ChangeDutyCycle(brightness)

GPIO.add_event_detect(SW3, GPIO.RISING, bouncetime=200, callback=pressSwitch)

try:
    while True:
        time.sleep(0.1)
        if GPIO.input(SW1) == GPIO.LOW:
            pressUp()
        elif GPIO.input(SW2) == GPIO.LOW:
            pressDown()
        if flag:
            sys.stdout.write("\rCurrent brightness: %d" %(brightness))
            sys.stdout.flush()

except KeyboardInterrupt:
    GPIO.cleanup()