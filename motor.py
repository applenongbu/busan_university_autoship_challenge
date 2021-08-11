from adafruit_servokit import ServoKit
import board
import busio
import time

def motorinit():
    print("i2c connetion initalzing")
    i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))
    global ship_servo_kit
    ship_servo_kit = ServoKit(channels=16, i2c=i2c_bus0)
    print("i2c connection initalzing finished")
    ship_servo_kit.servo[0].angle=90
    print("servo motor initalzing finished")
    print("BLDC motor calibrating")
    ship_servo_kit.servo[1].angle=90
    time.sleep(2)
    print("BLDC motor calibrating finished")
def servomove(degree):
    global ship_servo_kit
    ship_servo_kit.servo[0].angle=degree
    time.sleep(0.02)
def bldcmove(speed):
    global ship_servo_kit
    ship_servo_kit.servo[1].angle=speed
