import time

from BrickPi import *


class SelfDrivingCar(object):
    def __init__(self, speed, too_close):
        self.speed = -speed
        self.too_close = too_close
        self.setup()

    def setup(self):
        BrickPiSetup()  # setup the serial port for communication
        BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
        BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
        BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT
        BrickPiSetupSensors()   # Send the properties of sensors to BrickPi

    def eval_position(self):
        """Returns True if car should keep going straight False otherwise"""
        proximity = BrickPi.Sensor[PORT_1]
        if proximity <= self.too_close:
            print "The end of the world"
        print proximity

    def move(self):
        BrickPi.MotorSpeed[PORT_A] = self.speed  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = self.speed  #Set the speed of MotorB (-255 to 255)

    def drive(self):
        while True:
            # self.move()
            BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            print self.eval_position()

    def turn(self):
        """Turns the car 90 degrees"""
        return

if __name__ == "__main__":
    car = SelfDrivingCar(255, 20)
    car.drive()
