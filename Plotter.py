# Python library for Cyber Buggies Pen Plotter
from vex import *

def home():
    home_Xaxis()
    home_Yaxis()
    return 0

# ---------------------------------------------------------- #

def home_Xaxis():
    # Home Xaxis
    print("Homing Xaxis")
    Xaxis.set_velocity(50, PERCENT)
    Xaxis.spin(REVERSE)
    print("Waiting for first stop")
    while not Xstop.pressing():
       pass
    Xaxis.stop()
    print("Stopped")
    Xaxis.spin_for(FORWARD, 1, TURNS)
    print("Moving forward")
    Xaxis.set_velocity(20, PERCENT)
    Xaxis.spin(REVERSE)
    print("Waiting for second stop")
    while not Xstop.pressing():
        pass
    Xaxis.stop()
    print("Stopped")
    Xaxis.set_position(0,TURNS)
    print("Xaxis homing success!")
    return 0
    
# ---------------------------------------------------------- #

def home_Yaxis():
    # Home Yaxis
    print("Homing Yaxis")
    Yaxis.set_velocity(50, PERCENT)
    Yaxis.spin(REVERSE)
    print("Waiting for first stop")
    LeftStopped = False
    RightStopped = False
    while not(YstopLeft.pressing() and YstopRight.pressing()):
        if YstopLeft.pressing() and not(LeftStopped):
            Yaxis_motor_a.stop()
            LeftStopped = True
            print("Left Stopped")
        if YstopRight.pressing() and not(RightStopped):
            Yaxis_motor_b.stop()
            RightStopped = True
            print("Right Stopped")
    Yaxis.stop()
    print("Stopped")
    Yaxis.spin_for(FORWARD, 1, TURNS)
    print("Moving forward")
    Yaxis.set_velocity(20, PERCENT)
    Yaxis.spin(REVERSE)
    print("Waiting for second stop")
    LeftStopped = False
    RightStopped = False
    while not(YstopLeft.pressing() and YstopRight.pressing()):
        if YstopLeft.pressing() and not(LeftStopped):
            Yaxis_motor_a.stop()
            LeftStopped = True
            print("Left Stopped")
        if YstopRight.pressing() and not(RightStopped):
            Yaxis_motor_b.stop()
            RightStopped = True
            print("Right Stopped")
    Yaxis.stop()
    print("Stopped")
    Yaxis.set_position(0, TURNS)
    print("Yaxis homing success!")
    return 0

# ---------------------------------------------------------- #

def set_velocity(value):
    Xaxis.set_velocity(value, PERCENT)
    Yaxis.set_velocity(value, PERCENT)
    return value

# ---------------------------------------------------------- #

def set_zero_pos():
    Xaxis.set_position(0, TURNS)
    Yaxis.set_position(0, TURNS)

# ---------------------------------------------------------- #

ScaleFactor = 10

def get_ScaleFactor():
    global ScaleFactor
    return ScaleFactor

def set_ScaleFactor(new):
    global ScaleFactor
    ScaleFactor = new
    return ScaleFactor

# ---------------------------------------------------------- #

def get_position():
    global ScaleFactor
    x = Xaxis.position(DEGREES) * ScaleFactor
    y = Yaxis.position(DEGREES) * ScaleFactor
    return x, y

# ---------------------------------------------------------- #

def goto(x, y):
    Xaxis.spin_to_position((x * get_ScaleFactor), DEGREES)
    Yaxis.spin_to_position((y * get_ScaleFactor), DEGREES)
    return x, y

# ---------------------------------------------------------- #

def SetPenDown(input):
    if input == True:
        return 0
    elif input == False:
        return 0
    else:
        print("Invalid input for SetPen")
        return 1

# ---------------------------------------------------------- #