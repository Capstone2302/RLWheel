from __future__ import print_function
import cv2
import numpy as np
import time
from .data_logger import DataLogger_Ball


# Continuously capture frames from the camera
class BallDetector:
    lower_ball = np.array([10, 100, 10])  # BGR encoding
    upper_ball = np.array([90, 240, 120])  # BGR encoding
    kp = 10
    ki = 0.1
    kd = 1
    IM_WIDTH = 480
    IM_HEIGHT = 360
    FRAMERATE = 30
    loglength = 1000
    setpoint = IM_WIDTH / 2
    cutoff = 200

    def __init__(self):
        self.controlLoopTimes = [0] * 100
        self.positionLog = [0] * self.loglength
        self.errorsLog = [0] * self.loglength
        self.camera = cv2.VideoCapture(2, cv2.CAP_V4L2)
        self.start_time = time.time()
        self.prevPosition = self.setpoint
        self.position = self.setpoint
        self.speed = 0
        self.logger = DataLogger_Ball()

        if (self.camera == None) or (not self.camera.isOpened()):  # TODO: clean up
            print("\n\n")
            print("Error - could not open video device.")
            print("\n\n")
            exit(0)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.IM_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.IM_HEIGHT)
        self.camera.set(cv2.CAP_PROP_FPS, self.FRAMERATE)

    def errorFunc(x, x_dot):
        return 0.75 * BallDetector.gain(x) + 0.02 * x_dot

    def gain(x):
        return x

    def ball_finder(self, log):
        # returns error of ball position from setpoin
        _, frame = self.camera.read()

        blurred = cv2.GaussianBlur(frame, (3, 3), 0)

        colorMask = cv2.inRange(frame, BallDetector.lower_ball, BallDetector.upper_ball)

        contours, _ = cv2.findContours(
            colorMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M["m00"] != 0 and int(M["m01"] / M["m00"]) < self.cutoff:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            else:
                center = (int(BallDetector.setpoint), int(10))

            # To see the centroid clearly
            if radius > 2:
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # current position of ball
        try:
            delta = time.time() - self.start_time
            self.prevPosition = self.position
            self.position = center[0]
            speed = (self.prevPosition - self.position) / delta
        except:
            self.position = self.setpoint
            speed = 0
            delta = 0

        # Compute error
        error = self.setpoint - self.position

        # display the resulting frame
        cv2.line(
            frame, (int(self.setpoint), 0), (int(self.setpoint), 240), (255, 0, 0), 5
        )
        cv2.line(
            frame, (0, self.cutoff), (int(self.IM_WIDTH), self.cutoff), (255, 0, 0), 5
        )
        cv2.imshow("Color mask", colorMask)
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

        self.start_time = time.time()
        self.controlLoopTimes.insert(0, delta)
        self.controlLoopTimes.pop()
        self.positionLog.insert(0, self.position)
        self.positionLog.pop()

        self.errorsLog.insert(0, BallDetector.errorFunc(error, speed))
        self.errorsLog.pop()
        if log:
            self.logger.log_data(error, np.mean(self.controlLoopTimes), self.start_time)

        return error

    def exit(self, log):
        if log:
            self.logger.write_file()
