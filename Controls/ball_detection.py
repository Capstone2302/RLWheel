from __future__ import print_function
import cv2
import numpy as np
import time
import imutils
import sys

# Continuously capture frames from the camera
class BallDetector:
    lower_ball = np.array([0,0,0]) #BGR encoding
    upper_ball = np.array([120,120,120]) #BGR encoding
    setpoint = 120/2
    kp = 10
    ki = 0.1
    kd = 1
    IM_WIDTH = 640
    IM_HEIGHT = 480
    FRAMERATE = 30
    loglength = 1000

    def __init__(self):
        self.controlLoopTimes = [0] * 100
        self.positionLog = [0] * self.loglength
        self.errorsLog = [0] * self.loglength
        self.counter = 0
        self.camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.start_time = time.time()
        self.prevPosition = self.setpoint
        self.position = self.setpoint
        self.speed = 0

        if ((self.camera == None) or (not self.camera.isOpened())):
            print('\n\n')
            print('Error - could not open video device.')
            print('\n\n')
            exit(0)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.IM_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.IM_HEIGHT)
        self.camera.set(cv2.CAP_PROP_FPS, self.FRAMERATE)

        
    def errorFunc(x,x_dot):
        return 0.75*BallDetector.gain(x)+0.02*x_dot

    def gain(x):
        # if(x<-10):
        #     return -1*(1/32*x**2-3/8*x+25/8)
        # if(x<0):
        #     return x
        # if(x<10):
        #     return x
        # return 1/32*x**2+3/8*x+25/8
        return x
    def control_routine(self):
        _, frame = self.camera.read()

        blurred = cv2.GaussianBlur(frame, (3, 3), 0)

        colorMask = cv2.inRange(frame, BallDetector.lower_ball, BallDetector.upper_ball)

        contours, _ = cv2.findContours(colorMask, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M['m00'] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            else:
                center = (int(BallDetector.setpoint), int(120))

            # To see the centroid clearly
            if radius > 3:
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

        # Map output to PWM signal
        duty_cycle = BallDetector.errorFunc(error, speed)

        # display the resulting frame
        cv2.line(frame,(int(self.setpoint),0),(int(self.setpoint),240), (255,0,0),5)
        cv2.imshow('Color mask', colorMask)
        cv2.imshow('Frame',frame)
        cv2.waitKey(1)
        
        
        self.start_time = time.time()
        self.controlLoopTimes.insert(0,delta)
        self.controlLoopTimes.pop()
        self.positionLog.insert(0,self.position)
        self.positionLog.pop()
        
        self.errorsLog.insert(0,BallDetector.errorFunc(error, speed))
        self.errorsLog.pop()
        self.counter+=1
        if(self.counter%10==0):
            print("Average: " + str(np.mean(self.controlLoopTimes)) + 
                " s. Maximum: " + str(max(self.controlLoopTimes)) + 
                " s. Minimum: " + str(min(self.controlLoopTimes)) + "s"
                + " Pwm: " + str(duty_cycle) + "Error: " + str(error))
        #     if(self.counter%loglength==0):
        #         with open('/home/pi/Documents/WheelLogs/PositionLogs/PositionLog' + str(time.time_ns()) + '.txt', 'w') as tfile:
        #             tfile.write('Position' + 'n')
        #             tfile.write('\n'.join(str(x) for x in self.positionLog))
        #         with open('/home/pi/Documents/WheelLogs/ErrorLogs/ErrorLog' + str(time.time_ns()) + '.txt', 'w') as tfile:
        #             tfile.write('Error' + 'n')
        #             tfile.write('\n'.join(str(x) for x in self.errorsLog))
        # pass
        return error