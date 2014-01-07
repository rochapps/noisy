import time

from BrickPi import *


class SelfDrivingCar(object):

    def __init__(self, speed):
        self.speed = speed
        self.setup()

    def setup(self):
        BrickPiSetup()  # setup the serial port for communication
        BrickPi.MotorEnable[PORT_A] = 1 # Enable the Motor A
        BrickPi.MotorEnable[PORT_B] = 1 # Enable the Motor B
        BrickPiSetupSensors()   # Send the properties of sensors to BrickPi

    def move(self):
        while True:
            print "Running Forward"
            BrickPi.MotorSpeed[PORT_A] = self.speed  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = self.speed  #Set the speed of MotorB (-255 to 255)
            ot = time.time()
            while(time.time() - ot < 3):    #running while loop for 3 seconds
                BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
                time.sleep(.1)              # sleep for 100 ms
            print "Running Reverse"
            BrickPi.MotorSpeed[PORT_A] = -self.speed  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = -self.speed  #Set the speed of MotorB (-255 to 255)
            ot = time.time()
            while(time.time() - ot < 3):    #running while loop for 3 seconds
                BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
                time.sleep(.1)


if __name__ == "__main__":
    car = SelfDrivingCar(100)
    car.move()
