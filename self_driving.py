import time

from BrickPi import *


class ReflexDrivingCar(object):
    def __init__(self, speed, too_close):
        self.speed = speed
        self.too_close = too_close
        self.distances = []
        self.setup()

    def setup(self):
        BrickPiSetup()  # setup the serial port for communication
        BrickPi.MotorEnable[PORT_A] = 1  # Enable the Motor A
        BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
        BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT
        # BrickPi.Timeout = 1000  # 1 sec
        BrickPiSetupSensors()   # Send the properties of sensors to BrickPi

    def eval_position(self):
        """Returns True if car should keep going straight False otherwise"""
        proximity = BrickPi.Sensor[PORT_1]
        print proximity
        if proximity and proximity <= self.too_close:
            return False
        return True

    def move_forward(self):
        BrickPi.MotorSpeed[PORT_A] = self.speed  # Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = self.speed  # Set the speed of MotorB (-255 to 255)
        BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors

    def drive(self):
        while True:
            self.move_forward()
            self.turn()

    def turn(self):
        """Turns the car 90 degrees"""
        while not self.eval_position():
            BrickPi.MotorSpeed[PORT_A] = 255  # Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = -255  # Set the speed of MotorB (-255 to 255)
            BrickPiUpdateValues()
            time.sleep(0.1)

    def stop(self):
        """Stops moving car"""
        BrickPi.MotorSpeed[PORT_A] = 0  # Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = 0  # Set the speed of MotorB (-255 to 255)
        BrickPiUpdateValues()
        time.sleep(0.1)


if __name__ == "__main__":
    car = ReflexDrivingCar(255, 25)
    car.drive()
