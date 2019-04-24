import pygame

# Pedestrain object
class Pedestrian:

    waitingTime = 0
    x = 0
    y = 0
    speed = 0
    pedStartNum = 0

    def __init__(self, x, y, speed, waitingTime, line, pedStartNum):
        self.x = x
        self.y = y
        self.speed = speed
        self.waitingTime = waitingTime
        self.pedStartNum = pedStartNum

    def pedStart(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, 2.5, 2.5))
