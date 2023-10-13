import pygame
import pygame.camera
from pygame.locals import *
import time

# # initialize pygame
# pygame.init()
# pygame.camera.init()

# # set the resolution of the camera
# width = 640
# height = 480

# # create a new display surface
# screen = pygame.display.set_mode((width, height))

# # create a new camera instance
# cam = pygame.camera.Camera("/dev/video0", (width, height))

# # start the camera
# cam.start()

def display():
    # create a loop to capture and display images
    try:

        # initialize pygame
        pygame.init()
        pygame.camera.init()

        # set the resolution of the camera
        width = 640
        height = 480

        # create a new display surface
        screen = pygame.display.set_mode((width, height))

        # create a new camera instance
        cam = pygame.camera.Camera("/dev/video0", (width, height))

        # start the camera
        cam.start()
        while True:
            # capture an image
            image = cam.get_image()

            # draw the image on the screen
            screen.blit(image, (0, 0))
            pygame.display.update()
    except KeyboardInterrupt:
        return
