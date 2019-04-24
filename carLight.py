import pygame

# Car traffic light1 signal switching
def carTrafficLightSignalSwitching(carLight, screen, res_x, res_y, green, yellow, red):
    if carLight == "green":
        pygame.draw.rect(screen, green, (res_x * 0.377, res_y * 0.7, 15, 15))
    elif carLight == "greenToYellow" or carLight == "redToYellow":
        pygame.draw.rect(screen, yellow, (res_x * 0.377, res_y * 0.7, 15, 15))
    elif carLight == "red":
        pygame.draw.rect(screen, red, (res_x * 0.377, res_y * 0.7, 15, 15))
