import pygame
import random
import time
from background import Background
from color import Color
from car import Car
from pedestrian import Pedestrian
from checkCollision import isCarCollided, pedLightIsWalking
from carLight import carTrafficLightSignalSwitching
from pedLight import pedTrafficLightSignalSwitching

pygame.init()

# Set Simulator
clock = pygame.time.Clock()
running = True
simulatorSpeed = 1
waitingTime = 0
carLight = "green"
pedLight = "red"

# Traffic elements
carArray = []
pedArray = []
carLineArray = []

#Count TrafficModel Time
countCarLightTime = True
countPedLightTime = True
totalCarWaitingTime = 0
totalPedWaitingTime = 0
simStartTime = 0
if __name__ == "__main__":
    simStartTime = time.time()
    # Simulation Start
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        #Draw screen
        Background.screen.fill((255, 255, 255))
        Background.screen.blit(Background.image, (0, 0))

        # Draw title
        sys_font = pygame.font.SysFont("None", 30)
        rendered = sys_font.render("Traffic Model(Intelligent Traffic Light System)", 0, Color.black)
        Background.screen.blit(rendered, (Background.res_x * 0.05, Background.res_y * 0.05))
        # Draw road description(carLight, pedStart)
        sys_font = pygame.font.SysFont("None", 15)
        rendered = sys_font.render("carLight", 0, Color.black)
        Background.screen.blit(rendered, (Background.res_x * 0.375, Background.res_y * 0.725))
        rendered = sys_font.render("pedStart", 0, Color.black)
        Background.screen.blit(rendered, (Background.res_x * 0.3, Background.res_y * 0.725))
        # Draw video record area line
        pygame.draw.rect(Background.screen, (200, 0, 0), (Background.res_x * 0.498, Background.res_y * 0.48, 5, 200))
        rendered = sys_font.render("Car Record Line", 0, Color.black)
        # Draw video record area words
        sys_font = pygame.font.SysFont("None", 15)
        Background.screen.blit(rendered, (Background.res_x * 0.47, Background.res_y * 0.455))

        # Car traffic light1 signal switching
        carTrafficLightSignalSwitching(carLight, Background.screen, Background.res_x, Background.res_y, Color.green, Color.yellow, Color.red)

        # ped traffic light1 signal switching
        pedTrafficLightSignalSwitching(pedLight, Background.screen, Background.res_x, Background.res_y, Color.green, Color.darkGreen, Color.black, Color.red, simStartTime)

        # Count traffic flow at junction
        carCountAtCarLight = 0
        pedCountAtPedStart = 0
        for wCar in carArray:
            if 520 > wCar.x > 370:
                carCountAtCarLight += 1
        for ped in pedArray:
            if ped.y == Background.pedStart0YAry[0] and ped.pedStartNum == 0:
                pedCountAtPedStart += 1
            if ped.y == Background.pedStart0YAry[1] and ped.pedStartNum == 1:
                pedCountAtPedStart += 1
        sys_font = pygame.font.SysFont("None", 15)
        rendered = sys_font.render("Car at carLight: " + str(carCountAtCarLight), 0, Color.black)
        Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.7))
        rendered = sys_font.render("Ped at pedStart: " + str(pedCountAtPedStart), 0, Color.black)
        Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.73))

        # CarLight ITLS
        if countCarLightTime:
            carLightChgTime = time.time()
            countCarLightTime = False

        if carLight == "green" and (pedCountAtPedStart >= 20 or time.time() - carLightChgTime >= 120):
            carLight = "greenToYellow"
            # print("carLight switched to yellow.")
            # print("carLight status: " + carLight1 + ".\n")
            countCarLightTime = True

        elif carLight == "greenToYellow" and time.time() - carLightChgTime >= 3:
            carLight = "red"
            pedLight = "green"
            # print("carLight switched to red.")
            # print("carLight status: " + carLight + ".\n")
            countCarLightTime = True

        elif carLight == "red" and time.time() - carLightChgTime >= 13:
            carLight = "redToYellow"
            # print("carLight switched to yellow.")
            # print("carLight status: " + carLight + ".\n")
            countCarLightTime = True

        elif carLight == "red" and 12 >= time.time() - carLightChgTime >= 7:
            pedLight = "flashingGreen"

        elif carLight == "red" and time.time() - carLightChgTime > 9:
            pedLight = "red"

        elif carLight == "redToYellow" and time.time() - carLightChgTime >= 3:
            carLight = "green"
            # print("carLight switched to green.")
            # print("carLight status: " + carLight + ".\n")
            countCarLightTime = True

        # Put car on the road
        if random.randint(0, 20) == 1:
            line = random.randint(0, 3)
            c = Car(Background.res_x-100,Background.yArray[line], random.uniform(3, 8), 0, line) # The place that car start
            carArray.append(c)
            carLineArray.append([line, c])

        for c in carArray:
            if c.x > 150: # The place that car out
                c.carStart(Background.screen, Color.darkBlue) 

            if isCarCollided(carLineArray, c) and c.x > 210:
                c.x -= 0
                c.waitingTime += 1

        # Car postition
            else:
                # 1st part Route movement
                if c.x >= 588:
                    c.x -= c.speed
                # 2nd part Route movement
                elif 588 > c.x > 387:
                        c.x -= c.speed * 0.89    # slope of cars
                        c.y += c.speed * 0.11
                # Check 3rd part carlight junction movement
                elif 387 >= c.x > 377:
                    if carLight == "green":
                        if pedLightIsWalking(pedArray, Background.pedStart0YAry):
                            c.x -=0
                            c.waitingTime += 1
                        else:
                            c.x -= c.speed * 0.89
                            c.y += c.speed * 0.11
                    elif carLight == "greenToYellow" or carLight == "redToYellow":
                        if c.x >= 377:
                            c.x -= 0
                            c.waitingTime += 1
                        else:
                            c.x -= c.speed * 0.89
                            c.y += c.speed * 0.11
                    elif carLight == "red":
                            c.x -= 0
                            c.waitingTime += 1
                # 4rd part Route movement
                elif 377 >= c.x > 100:
                    c.x -= c.speed * 0.9
                    c.y += c.speed * 0.1


        # Put pedestrian on the road
        if random.randint(0, 25) == 1:
            line = random.randint(0, 3)
            pedStartNum = random.randint(0, 1)
            c = Pedestrian(Background.pedStart0XAry[line], Background.pedStart0YAry[pedStartNum], random.uniform(1, 1.5), 0, line, pedStartNum)
            pedArray.append(c)

        for p in pedArray:
            # pedStart0 to pedStart1
            if p.y >= Background.pedStart0YAry[1] and p.pedStartNum == 0:
                p.pedStart(Background.screen, Color.lightBlue)
                # Check Traffic light
                if pedLight == "red" and p.y == Background.pedStart0YAry[0]:
                    p.y -= 0
                    p.waitingTime += 1
                elif pedLight == "green" or p.y != Background.pedStart0YAry[0]:
                    p.y -= p.speed

            # pedStart1 to pedStart0
            if p.y <= Background.pedStart0YAry[0] and p.pedStartNum == 1:
                p.pedStart(Background.screen, Color.lightBlue)
                # Check Traffic light
                if pedLight == "red" and p.y == Background.pedStart0YAry[1]:
                    p.y += 0
                    p.waitingTime += 1
                elif pedLight == "green" or p.y != Background.pedStart0YAry[1]:
                    p.y += p.speed


        # Print pedestrian number
        for ped in pedArray:
            if ped.y == Background.pedStart0YAry[0] and ped.pedStartNum == 0:
                Background.pedStart[0] += 1
            if ped.y == Background.pedStart0YAry[1] and ped.pedStartNum == 1:
                Background.pedStart[1] += 1

        sys_font = pygame.font.SysFont("None", 16)

        rendered = sys_font.render(str(Background.pedStart[0]), 0,(35, 20, 245))
        Background.screen.blit(rendered, (Background.res_x * 0.335, Background.res_y * 0.71))

        rendered = sys_font.render(str(Background.pedStart[1]), 0, (35, 20, 245))
        Background.screen.blit(rendered, (Background.res_x * 0.335, Background.res_y * 0.546))

        rendered = sys_font.render(str(Background.pedStart[2]), 0, (35, 20, 245))
        Background.screen.blit(rendered, (Background.res_x * 0.34, Background.res_y * 0.505))

        Background.pedStart[0] = 0
        Background.pedStart[1] = 0

        # Update Game
        clock.tick(30)
        pygame.display.update()
# Print Simulation data
print()
print("Simulation has run for " + str(time.time() - simStartTime) + " second(s)")

print("Total car number on the street: " + str(len(carArray)))
for car in carArray:
    totalCarWaitingTime += car.waitingTime
print("Average car watiting time: " + str(totalCarWaitingTime / len(carArray) / 30) + " seconds")

print("Total pedestrian number on the street: " + str(len(pedArray)))
for ped in pedArray:
    totalPedWaitingTime += ped.waitingTime
print("Average pedestrian watiting time: " + str(totalPedWaitingTime / len(carArray) / 30) + " seconds")
