import pygame
import time

# ped traffic light1 signal switching
def pedTrafficLightSignalSwitching(pedLight, screen, res_x, res_y, green, darkGreen, black, red, simStartTime, simTime):

    if pedLight == "green":
        pygame.draw.rect(screen, green, (res_x * 0.348, res_y * 0.703, 10, 10))
    elif pedLight == "flashingGreen" or pedLight == "flashingGreenLonger":
        if (int(simTime)) % 2 > 0:
            pygame.draw.rect(screen, darkGreen, (res_x * 0.348, res_y * 0.703, 10, 10))
        else:
            pygame.draw.rect(screen, black, (res_x * 0.348, res_y * 0.703, 10, 10))
    elif pedLight == "red" or pedLight == "bufferRed":
        pygame.draw.rect(screen, red, (res_x * 0.348, res_y * 0.703, 10, 10))
