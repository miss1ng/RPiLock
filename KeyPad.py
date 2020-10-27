from gpiozero import Button
from events import Events

class KeyPad():
    def __init__(self, pinBtn1, pinBtn2, pinBtn3, pinBtn4, pinBtn5, pinBtnShift, pinBtnSubmit):
        self.events = Events(('keyPressed', 'pwdSubmitted', 'onShiftPressed', 'resetPass'))
        self.pwdFields = []
        self.inShiftMode = False
        self.inResetMode = False
        self.lockState = 0
        self.resetType = False
        
        self.btn1 = Button(pinBtn1, bounce_time=0.02)
        self.btn2 = Button(pinBtn2, bounce_time=0.02)
        self.btn3 = Button(pinBtn3, bounce_time=0.02)
        self.btn4 = Button(pinBtn4, bounce_time=0.02)
        self.btn5 = Button(pinBtn5, bounce_time=0.02)
        self.btnShift = Button(pinBtnShift, bounce_time=0.02)
        self.btnSubmit = Button(pinBtnSubmit, bounce_time=0.02)
 
        self.btn1.when_pressed = self.press1
        self.btn2.when_pressed = self.press2
        self.btn3.when_pressed = self.press3
        self.btn4.when_pressed = self.press4
        self.btn5.when_pressed = self.press5
        self.btnShift.when_pressed = self.pressShift
        self.btnSubmit.when_pressed = self.pressSubmit

    def isPwdReady(self):
        if len(self.pwdFields) >= 6:
            return True
        return False
    
    def getPwd(self):
        if len(self.pwdFields) > 6:
            return self.pwdFields[-6:]
        else:
            return self.pwdFields[:]
    
    def setShiftMode(self, mode):
        self.inShiftMode = mode
        
    def setResetType(self, type):
        if type == 1:
            self.inResetMode = False
            self.resetType = False
        else:
            self.resetType = True

    def reset(self):
        self.pwdFields = []

    # Key events
    def press1(self):
        self.pwdFields.append(2 if (self.inShiftMode) else 1)
        self.events.keyPressed()

    def press2(self):
        self.pwdFields.append(4 if (self.inShiftMode) else 3)
        self.events.keyPressed()

    def press3(self):
        self.pwdFields.append(6 if (self.inShiftMode) else 5)
        self.events.keyPressed()

    def press4(self):
        self.pwdFields.append(8 if (self.inShiftMode) else 7)
        self.events.keyPressed()

    def press5(self):
        self.pwdFields.append(0 if (self.inShiftMode) else 9)
        self.events.keyPressed()

    def pressShift(self):
        self.events.onShiftPressed()

    def pressSubmit(self):
        if self.inShiftMode:
            if self.lockState == 0 and self.inResetMode == False:
                self.inResetMode = True
                print("Reset mode enabled. Type the 6-digit password and press [Submit] to reset the password")
                return
            else:
                if self.lockState == 0 and self.inResetMode == True:
                    if len(self.getPwd()) == 6:
                        #print("length is 6!")
                        self.events.resetPass(self.resetType)
                        return
                    else:
                        print("[Reset] Password too short!")
                        return
                else:
                    print("Locked.Reset mode is disabled")
        else:
            if len(self.pwdFields) < 6 and len(self.pwdFields) > 0:
                print("Password too short!")
            self.events.pwdSubmitted()