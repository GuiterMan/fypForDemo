import pygame

# Car object
class Car:
    waitingTime = 0
    x = 0
    y = 0
    speed = 0
    line = 0

    def __init__(self, x, y, speed, waitingTime, line):
        self.waitingTime = 0
        self.x = x
        self.y = y
        self.speed = speed
        self.waitingTime = waitingTime
        self.line =line
    def carStart(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, 24, 12))

        # pygame.draw.rect(screen, darkBlue, (self.x, self.y, 40, 20))

