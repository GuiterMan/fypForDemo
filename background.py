import pygame

# Draw screen data
class Background:
    res_x = 1024
    res_y = 768
    screen = pygame.display.set_mode((res_x , res_y))
    image = pygame.image.load("rdbg.png")

    # Pedstrian startPosition array
    pedStart = [0, 0, 0]
    pedStart0XAry = [res_x * 0.35, res_x * 0.355, res_x * 0.36, res_x * 0.365]
    pedStart0YAry = [res_y * 0.695, res_y * 0.5695]

    # Car start Y position
    yArray = [res_y * 0.654, res_y * 0.63, res_y * 0.604, res_y * 0.578]