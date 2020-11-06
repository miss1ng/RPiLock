from KeyPad import *
import RPi.GPIO as GPIO
import time, os

UNLOCKED = 0
LOCKED = 1
state = LOCKED
password = []
isShiftPressed = False

relay = 4
relayLED = 5
ShiftLED = 6
SW1 = 17
SW2 = 18
SW3 = 27
SW4 = 22
SW5 = 23
SW_shift = 24
SW_submit = 25

kp = KeyPad(SW1, SW2, SW3, SW4, SW5, SW_shift, SW_submit)

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayLED, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(relay, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ShiftLED, GPIO.OUT, initial=GPIO.LOW)

def initData():
    global password
    fp = open("password.txt", "r")
    password = fp.readline()
    fp.close()

def saveData():
    global password
    fp = open("password.txt", "w")
    fp.write(password)
    fp.close()

def setState(st):
    global state
    kp.lockState = st
    state = st

def lock():
    global state
    GPIO.output(relay, GPIO.LOW)
    # Flash 3 times
    for i in range(1, 6):
        time.sleep(0.2)
        GPIO.output(relayLED, bool(i % 2))
    GPIO.output(relayLED, GPIO.LOW)
    kp.reset()
    setState(LOCKED)
    print("Locked")

def unlock():
    global state
    GPIO.output(relay, GPIO.HIGH)
    GPIO.output(relayLED, GPIO.LOW)
    kp.reset()
    setState(UNLOCKED)
    print("Unlocked")

def shiftPressed():
    global isShiftPressed
    isShiftPressed = not isShiftPressed
    kp.setShiftMode(isShiftPressed)
    if isShiftPressed:
        # print("Shift pressed")
        GPIO.output(ShiftLED, GPIO.HIGH)
    else:
        # print("Shift unpressed")
        GPIO.output(ShiftLED, GPIO.LOW)
    # kp.KP_DebugPrint()

def resetPwd(st):
    global password
    tmp = [str(i) for i in kp.getPwd()]
    pwd = ''.join(tmp)
    kp.reset()
    if st == False:
        password = pwd
        kp.setResetType(0)
        print("Reset password to %s, please check again" % password)
        return
    else:
        if password == pwd:
            saveData()
            print("Saved")
        else:
            for i in range(1, 6):
                time.sleep(0.2)
                GPIO.output(relayLED, bool(i % 2))
            GPIO.output(relayLED, GPIO.LOW)
            print("Save failed.")
            initData()
        kp.setResetType(1)

    shiftPressed()

def display():
    print(kp.getPwd())

def checkPwd():
    tmp = [str(i) for i in kp.getPwd()]
    pwdF = ''.join(tmp)
    if pwdF.strip() == password.strip():
        unlock()
    else:
        print("Invalid password")
        lock()
    kp.setResetType(1)

kp.events.keyPressed += display
kp.events.onShiftPressed += shiftPressed
kp.events.pwdSubmitted += checkPwd
kp.events.resetPass += resetPwd

def Lock_Init():
    initData()
    lock()

try:
    time.sleep(0.3)
    Lock_Init()
    
    while True:
        pass

except KeyboardInterrupt:
    saveData()
    # GPIO.cleanup()