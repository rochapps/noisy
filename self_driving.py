import random
import time

from BrickPi import BrickPi, BrickPiSetup, BrickPiSetupSensors, BrickPiUpdateValues, \
    PORT_A, PORT_B, PORT_1, TYPE_SENSOR_ULTRASONIC_CONT


class ReflexDrivingCar(object):
    def __init__(self, speed=255):
        self.speed = speed  # (-255 to 255)
        self.too_close = 25
        self.setup()

    def drive(self):
        while True:
            turn_direction = random.choice(["left", "right"])
            while self.continue_moving:
                # Move forward while there is nothing too close ahead.
                self.move_forward()
                time.sleep(0.1)
            while not self.continue_moving:
                # Turn once you get too close to an object.
                self.turn(direction=turn_direction)
                time.sleep(0.1)

    @property
    def continue_moving(self):
        """Returns True if car should keep moving forward or false if it should turn."""
        proximity = BrickPi.Sensor[PORT_1]
        if proximity and proximity <= self.too_close:
            return False
        return True

    def move_forward(self):
        """Moves the car forward."""
        BrickPi.MotorSpeed[PORT_A] = self.speed
        BrickPi.MotorSpeed[PORT_B] = self.speed
        BrickPiUpdateValues()

    @staticmethod
    def setup():
        """Enables the motors and sensors for use."""
        BrickPiSetup()
        BrickPi.MotorEnable[PORT_A] = 1
        BrickPi.MotorEnable[PORT_B] = 1
        BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT
        BrickPiSetupSensors()
        BrickPiUpdateValues()

    @staticmethod
    def stop():
        """Stops the car."""
        BrickPi.MotorSpeed[PORT_A] = 0  # Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_B] = 0  # Set the speed of MotorB (-255 to 255)
        BrickPiUpdateValues()

    @staticmethod
    def turn(direction="right"):
        """Turns the car until there is nothing in front of it."""
        if direction == "right":
            BrickPi.MotorSpeed[PORT_A] = 255  # Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = -255  # Set the speed of MotorB (-255 to 255)
            BrickPiUpdateValues()
        else:
            BrickPi.MotorSpeed[PORT_A] = -255  # Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_B] = 255  # Set the speed of MotorB (-255 to 255)
            BrickPiUpdateValues()


if __name__ == "__main__":
    car = ReflexDrivingCar()
    car.drive()
