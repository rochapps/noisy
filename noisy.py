import random
import time

from BrickPi import BrickPi, BrickPiSetup, BrickPiSetupSensors, BrickPiUpdateValues, \
    PORT_A, PORT_B, PORT_1, TYPE_SENSOR_ULTRASONIC_CONT


class SelfDrivingRobot(object):
    """
    Self Driving robot that uses a reflex agent to avoid objects around him.
    """
    def __init__(self, speed=255):
        self.speed = speed  # (-255 to 255)
        self.turn_direction = random.choice(["left", "right"])
        self.setup()

    def drive(self):
        """Drives the robot around his environment."""
        while True:
            action = self.get_action()
            self.move(action=action)
            BrickPiUpdateValues()
            time.sleep(0.1)

    def get_action(self):
        """Returns the direction in which the robot needs to move"""
        proximity = BrickPi.Sensor[PORT_1]
        if proximity and proximity > 25:
            return "forward"
        elif proximity and 5 < proximity <= 25:
            return self.turn_direction
        else:
            return "backwards"

    def move(self, action="forward"):
        """Adjust motors speeds."""
        if action == "forward":
            BrickPi.MotorSpeed[PORT_A] = self.speed
            BrickPi.MotorSpeed[PORT_B] = self.speed
        elif action == "backwards":
            BrickPi.MotorSpeed[PORT_A] = -self.speed
            BrickPi.MotorSpeed[PORT_B] = -self.speed
        elif action == "right":
            BrickPi.MotorSpeed[PORT_A] = self.speed
            BrickPi.MotorSpeed[PORT_B] = -self.speed
        elif action == "left":
            BrickPi.MotorSpeed[PORT_A] = -self.speed
            BrickPi.MotorSpeed[PORT_B] = self.speed

    @staticmethod
    def setup():
        """Enables the motors and sensors for use."""
        BrickPiSetup()
        BrickPi.MotorEnable[PORT_A] = 1
        BrickPi.MotorEnable[PORT_B] = 1
        BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT
        BrickPiSetupSensors()
        BrickPiUpdateValues()


if __name__ == "__main__":
    robot = SelfDrivingRobot()
    robot.drive()
