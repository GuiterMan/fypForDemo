import pygame
import random
import time
import openpyxl
import threading
import os
from background import Background
from color import Color
from car import Car
from pedestrian import Pedestrian
from checkCollision import isTooCloseToCarInFront, isCarCollided, pedLightIsWalking, line56IsCarCollided
from carLight import carTrafficLightSignalSwitching
from pedLight import pedTrafficLightSignalSwitching


def main_sim(threshold1, threshold2, threshold3, threshold4, threshold5, threshold6, threshold7):
    pygame.init()

    # Set Simulator changeable variable
    itlsMode = True  # Use ITLS mode or Normal Light
    simulatorSpeed = 1  # Simulator speed (default = 1)
    totalCarNum = 2000 / 6  # How many car generate in the sim period (2000 to 3000)
    totalPedNum = 623 / 6  # How many pedestrian generate in the sim period (623)
    totalGrandMotherNum = 12 / 6  # How many grandmother generate in the sim period
    simTimePeriod = 3600 / 6  # How long the simulation run (in sec)

    carMaxNumAtJunction = threshold1  # Max number of pedstrain wait at junction (default = 15)
    carLightGreenMinTime = threshold2  #The least Carlight Green time last (default = 10)
    carMaxWaitingtimeAtJunction = threshold3 # Switch light if a car wait more than x sec (default = 30)(Must Be > 16)

    pedMaxNumAtJunction = threshold4  # Max number of pedstrain wait at junction (default = 20)
    pedLightGreenMinTime = threshold5  # The least Carlight Green time last (default = 10)
    pedMaxWaitingtimeAtJunction = threshold6 # Switch light if a ped wait more than x sec (default = 30)

    pedLightFlashLongerTime = threshold7  # Exetend Flashing Green Time for pedLight (default = 6)

    carLightGreenMaxTime = simTimePeriod  # Car green light max time (For fixing bug only)
    pedLightGreenMaxTime = simTimePeriod  # Car green light max time (For fixing bug only)

    # No need to change (just calculation)
    carGenRate = (simTimePeriod * 30) / totalCarNum  # sec * frames / total carNum
    pedGenRate = (simTimePeriod * 30) / totalPedNum  # sec * frames / total carNum
    grandMotherGenRate = (simTimePeriod * 30) / totalGrandMotherNum

    # Set Simulator counting variable
    clock = pygame.time.Clock()
    running = True
    waitingTime = 0
    carLight = "green"
    pedLight = "red"
    frameCount = 0
    simTime = 0

    # 1400 / (3600 * 30)

    # Traffic elements
    carArray = []
    pedArray = []
    carLineArray = []
    carArray2 = []
    carArray3 = []
    carArray4 = []
    carLineArray2 = []
    carLineArray3 = []
    carLineArray4 = []

    # Count TrafficModel Time
    countCarLightTime = True # For Carlight switch
    countPedLightTime = True # For Pedlight switch
    countCarWaitAtJunctionTime = True # For counting car waiting at junction
    countPedWaitAtJunctionTime = False # For counting ped waiting at junction
    carWaitingtimeAtJunctionTimeStamp = 0
    pedWaitingtimeAtJunctionTimeStamp = 0
    carWaitingtimeAtJunction = 0
    pedWaitingtimeAtJunction = 0
    totalCarWaitingTime = 0
    totalPedWaitingTime = 0

    simStartTime = 0
    if __name__ == "__main__":

        # count real time
        simStartTime = time.time()

        # Simulation Start
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            # set simulation time period
            if int(simTime) == simTimePeriod:
                running = False

            # count Frame pass in scale
            simTime = frameCount / 30
            frameCount += 1 * simulatorSpeed
            # Draw screen
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
            # Draw data area
            pygame.draw.rect(Background.screen, (180, 180, 180), (Background.res_x * 0.49, Background.res_y * 0.75, 450, 150))
            rendered = sys_font.render("Car Record Line", 0, Color.black)
            sys_font = pygame.font.SysFont("None", 20)
            rendered = sys_font.render("ITLS data: ", 0, Color.black)
            Background.screen.blit(rendered, (Background.res_x * 0.5, Background.res_y * 0.76))
            # Draw simulation time
            sys_font = pygame.font.SysFont("None", 20)
            rendered = sys_font.render("Simulation time: " + str(round(simTime, 2)) + " sec.", 0, Color.black)
            Background.screen.blit(rendered, (Background.res_x * 0.05, Background.res_y * 0.15))
            # Draw simulation running speed
            rendered = sys_font.render("Simulation running at " + str(simulatorSpeed) + "X speed.", 0, Color.black)
            Background.screen.blit(rendered, (Background.res_x * 0.05, Background.res_y * 0.1))
            # Car traffic light1 signal switching
            carTrafficLightSignalSwitching(carLight, Background.screen, Background.res_x, Background.res_y, Color.green,
                                           Color.yellow, Color.red)

            # ped traffic light1 signal switching
            pedTrafficLightSignalSwitching(pedLight, Background.screen, Background.res_x, Background.res_y, Color.green,
                                           Color.darkGreen, Color.black, Color.red, simStartTime, simTime)

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
            sys_font = pygame.font.SysFont("None", 16)
            rendered = sys_font.render("Car at carLight: " + str(carCountAtCarLight), 0, Color.black)
            Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.79))
            rendered = sys_font.render("Ped at pedStart: " + str(pedCountAtPedStart), 0, Color.black)
            Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.81))

            # CarLight ITLS
            if itlsMode == True:
                if countCarLightTime:
                    carLightChgTime = simTime
                    countCarLightTime = False
                if countPedLightTime:
                    pedLightChgTime = simTime
                    countPedLightTime = False

                if (carCountAtCarLight > 0) and (countCarWaitAtJunctionTime == True) and (carLight == "red"): # At least one car waiting at intersection
                    carWaitingtimeAtJunctionTimeStamp = simTime
                    countCarWaitAtJunctionTime = False

                if (countCarWaitAtJunctionTime == False) and (carLight == "red"):
                    carWaitingtimeAtJunction = simTime - carWaitingtimeAtJunctionTimeStamp
                else:
                    carWaitingtimeAtJunction = 0
                if (pedCountAtPedStart > 0) and (countPedWaitAtJunctionTime == True) and ((pedLight == "red") or (pedLight == "flashingGreen")):  # At least one ped waiting at intersection
                    pedWaitingtimeAtJunctionTimeStamp = simTime
                    countPedWaitAtJunctionTime = False

                if (countPedWaitAtJunctionTime == False) and (pedCountAtPedStart > 0) and ((pedLight == "red") or (pedLight == "flashingGreen")):
                    pedWaitingtimeAtJunction = simTime - pedWaitingtimeAtJunctionTimeStamp
                else:
                    pedWaitingtimeAtJunction = 0

                if (carLight == "green" and
                        (((simTime - carLightChgTime >= carLightGreenMinTime) and ((pedCountAtPedStart >= pedMaxNumAtJunction) or (pedWaitingtimeAtJunction > pedMaxWaitingtimeAtJunction))) or (simTime - carLightChgTime >= carLightGreenMaxTime))):  # CarLight switch to red conditiion
                    carLight = "greenToYellow"
                    # print("carLight switched to yellow.")
                    # print("carLight status: " + carLight1 + ".\n")
                    countCarLightTime = True

                elif carLight == "greenToYellow" and simTime - carLightChgTime >= 3:  # Light yellow last for 3 second
                    carLight = "red"
                    pedLight = "green"
                    # print("carLight switched to red.")
                    # print("carLight status: " + carLight + ".\n")
                    countCarLightTime = True
                    countCarWaitAtJunctionTime = True
                    countPedLightTime = True

                elif (pedLight == "green" and
                    (((simTime - pedLightChgTime >= carLightGreenMinTime) and ((carCountAtCarLight >= carMaxNumAtJunction) or (carWaitingtimeAtJunction > carMaxWaitingtimeAtJunction))) or (simTime - pedLightChgTime >= pedLightGreenMaxTime))):  # CarLight switch to red conditiion

                    pedLight = "flashingGreen"
                    countPedWaitAtJunctionTime = True
                    countPedLightTime = True

                elif pedLight == "flashingGreen" and simTime - pedLightChgTime > 10:
                    if pedLightIsWalking(pedArray, Background.pedStart0YAry):
                        pedLight = "flashingGreenLonger"
                    else:
                        pedLight = "red"
                        carLight = "redToYellow"
                        countCarLightTime = True

                elif pedLight == "flashingGreenLonger" and simTime - pedLightChgTime > (10 + pedLightFlashLongerTime):
                    pedLight = "red"
                    carLight = "redToYellow"
                    countCarLightTime = True


                elif carLight == "redToYellow" and simTime - carLightChgTime >= 3:
                    carLight = "green"
                    # print("carLight switched to green.")
                    # print("carLight status: " + carLight + ".\n")
                    countCarLightTime = True

            # Normal Traffic Light Switching
            if itlsMode == False:

                if countCarLightTime:
                    carLightChgTime = simTime
                    countCarLightTime = False

                if carLight == "green" and simTime - carLightChgTime >= 86:  # 86
                    carLight = "greenToYellow"
                    # print("carLight1 switched to yellow.")
                    # print("carLight1 status: " + carLight1 + ".\n")
                    countCarLightTime = True

                elif carLight == "greenToYellow" and simTime - carLightChgTime >= 3:
                    carLight = "red"
                    # print("carLight1 switched to red.")
                    # print("carLight1 status: " + carLight1 + ".\n")
                    countCarLightTime = True

                elif carLight == "red" and simTime - carLightChgTime >= 39:  # 39
                    carLight = "redToYellow"
                    # print("carLight1 switched to yellow")
                    # print("carLight1 status: " + carLight1 + ".\n")
                    countCarLightTime = True

                elif carLight == "redToYellow" and simTime - carLightChgTime >= 3:
                    carLight = "green"
                    # print("carLight1 switched to green")
                    # print("carLight1 status: " + carLight1 + ".\n")
                    countCarLightTime = True

                # Ped light normal switch
                if countPedLightTime:
                    pedLightChgTime = simTime
                    countPedLightTime = False

                if pedLight == "red" and simTime - pedLightChgTime >= 92:  # 92
                    pedLight = "green"
                    # print("pedLight1 switched to green.")
                    # print("pedLight1 status: " + pedLight1 + ".\n")
                    countPedLightTime = True

                elif pedLight == "green" and simTime - pedLightChgTime >= 23:  # 23
                    pedLight = "flashingGreen"
                    # print("pedLight1 switched to red.")
                    # print("pedLight1 status: " + pedLight1 + ".\n")
                    countPedLightTime = True

                elif pedLight == "flashingGreen" and simTime - pedLightChgTime >= 10:  # 10
                    pedLight = "bufferRed"
                    # print("pedLight1 switched to yellow")
                    # print("pedLight1 status: " + pedLight1 + ".\n")
                    countPedLightTime = True

                elif pedLight == "bufferRed" and simTime - pedLightChgTime >= 6:  # 3 + 3
                    pedLight = "red"
                    # print("pedLight1 switched to yellow")
                    # print("pedLight1 status: " + pedLight1 + ".\n")
                    countPedLightTime = True

            # Put car on the road
            if random.randint(0, int(carGenRate / simulatorSpeed / 2)) == 1:
                line = random.randint(0, 3)
                if random.randint(0, 10) == 1:
                    c = Car(Background.res_x - 100, Background.yArray[line], random.uniform(2, 4) * simulatorSpeed, 0,
                            line, True)  # The place that car start
                else:
                    c = Car(Background.res_x - 100, Background.yArray[line], random.uniform(2, 4) * simulatorSpeed, 0,
                        line, False)  # The place that car start

                carArray.append(c)
                carLineArray.append([line, c, c.isBus])

            for c in carArray:
                if c.x > 100 and c.isBus:  # The place that car out
                    c.busStart(Background.screen, Color.darkBlue)
                elif c.x > 100 and not(c.isBus):
                    c.carStart(Background.screen, Color.darkBlue)

                if isTooCloseToCarInFront(carLineArray, c) and c.x > 150:
                    c.speed = 1.5 * simulatorSpeed
                else:
                    c.speed = random.uniform(3, 4) * simulatorSpeed

                if isCarCollided(carLineArray, c) and c.x > 150:
                    c.x -= 0
                    c.waitingTime += 1 * simulatorSpeed

                # Car postition
                else:
                    # 1st part Route movement
                    if c.x >= 588:
                        c.x -= c.speed
                    # 2nd part Route movement
                    elif 588 > c.x > 395:
                        c.x -= c.speed * 0.97  # slope of cars
                        c.y += c.speed * 0.03
                    # Check 3rd part carlight junction movement
                    elif 395 >= c.x > 360:
                        if carLight == "green":
                            if pedLightIsWalking(pedArray, Background.pedStart0YAry):
                                c.x -= 0
                                c.waitingTime += 1 * simulatorSpeed
                            else:
                                c.x -= c.speed * 0.97
                                c.y += c.speed * 0.03
                        elif carLight == "greenToYellow" or carLight == "redToYellow":
                            if c.x >= 360:
                                c.x -= 0
                                c.waitingTime += 1 * simulatorSpeed
                            else:
                                c.x -= c.speed * 0.97
                                c.y += c.speed * 0.03
                        elif carLight == "red":
                            c.x -= 0
                            c.waitingTime += 1 * simulatorSpeed
                    # 4rd part Route movement
                    elif 360 >= c.x > 100:
                        c.x -= c.speed * 0.91
                        c.y += c.speed * 0.09

            # Put Car on the road 6th line(For demo)
            if random.randint(0, int(carGenRate / simulatorSpeed/ 2 * 5)) == 1:
                line2 = 1
                c2 = Car(Background.res_x - 100, Background.yArray2[1], random.uniform(2, 4) * simulatorSpeed, 0,
                        line2, False)  # The place that car start
                carArray2.append(c2)
                carLineArray2.append([line2, c2])

            for c2 in carArray2:
                if c2.x > 100 and c2.y > 400:  # The place that car out
                    c2.carStartImg(Background.screen)

                if line56IsCarCollided(carLineArray2, c2) and (c2.x > 150 and c2.y > 400):
                        print("collided")
                        pygame.draw.rect(Background.screen, (200, 0, 0),
                                         (500, 400, 150, 1))
                        c2.x -= 0
                else:

                    # Car postition

                    # 1st part Route movement
                    if c2.x >= 588 and 400 <= c2.y:
                        c2.x -= c2.speed
                    # 2nd part Route movement
                    elif 588 > c2.x > 470 and 400 <= c2.y:
                        c2.x -= 4 * 0.97  # slope of cars
                        c2.y += 4 * 0.03
                    # Check 3rd part carlight junction movement
                    elif 470 >= c2.x > 465 and 400 <= c2.y:
                        if carLight == "green":
                            if pedLightIsWalking(pedArray, Background.pedStart0YAry):
                                c2.x -= 0
                                c2.waitingTime += 1 * simulatorSpeed
                            else:
                                c2.x -= 4 * 0.97
                                c2.y += 4 * 0.03
                        elif carLight == "greenToYellow" or carLight == "redToYellow":
                            if c2.x >= 360:
                                c2.x -= 0
                                c2.waitingTime += 1 * simulatorSpeed
                            else:
                                c2.x -= 4 * 0.97
                                c2.y += 4 * 0.03
                        elif carLight == "red":
                            c2.x -= 0
                            c2.waitingTime += 1 * simulatorSpeed
                    # 4th part Route movement
                    elif 465 >= c2.x >= 440 and 400 <= c2.y:
                        pygame.draw.rect(Background.screen, (200, 0, 0),
                                             (500, 370, 150, 1))
                        c2.x -= 4 * 0.37
                        c2.y += 4 * -0.63
                    elif 470 >= c2.x >= 410 and 400 >= c2.y >= 360:
                        c2.carStartImgAndRotate(Background.screen)
                        c2.x -= 4 * 0.5
                        c2.y += 4 * -0.5
                    elif 120 <=c2.y <= 360:
                        c2.carStartImgAndRotate2(Background.screen)
                        c2.x -= 4 * -0.39
                        c2.y += 4 * -0.61


            # Put Car on the road 5th line(For demo)
            if random.randint(0, int(carGenRate / simulatorSpeed * 5)) == 1:
                line3 = 0
                c3 = Car(Background.res_x - 100, Background.yArray2[0], random.uniform(2, 4) * simulatorSpeed, 0,
                        line3, False)  # The place that car start
                carArray3.append(c3)
                carLineArray3.append([line3, c3])


            for c3 in carArray3:
                if c3.x > 100 and c3.y > 415:  # The place that car out
                    c3.carStartImg(Background.screen)
                if line56IsCarCollided(carLineArray3, c3) and (c3.x > 150 and c3.y > 400):
                    print("collided")
                    pygame.draw.rect(Background.screen, (200, 0, 0),
                                     (500, 400, 150, 1))
                    c3.x -= 0

                else:

                # Car postition

                    # 1st part Route movement
                    if c3.x >= 588 and 415 <= c3.y:
                        c3.x -= c3.speed
                    # 2nd part Route movement
                    elif 588 > c3.x > 470 and 415 <= c3.y:
                        c3.x -= 4 * 0.97  # slope of cars
                        c3.y += 4 * 0.03
                    # Check 3rd part carlight junction movement
                    elif 470 >= c3.x > 443 and 415 <= c3.y:
                        if carLight == "green":
                            if pedLightIsWalking(pedArray, Background.pedStart0YAry):
                                c3.x -= 0
                                c3.waitingTime += 1 * simulatorSpeed
                            else:
                                c3.x -= 4.5 * 0.97
                                c3.y += 4.5 * 0.03
                        elif carLight == "greenToYellow" or carLight == "redToYellow":
                            if c3.x >= 360:
                                c3.x -= 0
                                c3.waitingTime += 1 * simulatorSpeed
                            else:
                                c3.x -= 4.5 * 0.97
                                c3.y += 4.5 * 0.03
                        elif carLight == "red":
                            c3.x -= 0
                            c3.waitingTime += 1 * simulatorSpeed
                    # 4th part Route movement
                    elif 445 >= c3.x >= 430 and 415 <= c3.y:
                        pygame.draw.rect(Background.screen, (200, 0, 0),
                                         (500, 370, 150, 1))
                        c3.x -= 4.5 * 0.34
                        c3.y += 4.5 * -0.63
                    elif 470 >= c3.x >= 350 and 415 >= c3.y >= 360:
                        c3.carStartImgAndRotate(Background.screen)
                        c3.x -= 4.5 * 0.40
                        c3.y += 4.5 * -0.65
                    elif 120 <= c3.y <= 360:
                        c3.carStartImgAndRotate2(Background.screen)
                        c3.x -= 4.5 * -0.39
                        c3.y += 4.5 * -0.61

            # Put Car on left in rd
            if random.randint(0, int(carGenRate / simulatorSpeed * 10)) == 1:
                line4 = 0
                c4 = Car(50, 453, 3 * simulatorSpeed, 0,
                        line4, False)  # The place that car start
                carArray4.append(c4)
                carLineArray4.append([line4, c4])

            for c4 in carArray4:
                if c4.x >= 50 and c4.y >= 434:  # The place that car out
                    c4.carStartImg(Background.screen)

                    c4.x += 5 * 0.93
                    c4.y -= 5 * 0.07

                elif c4.x >= 50 and 434 >= c4.y >= 370:
                    c4.carStartImgAndRotate2(Background.screen)
                    c4.x += 5 * 0.50
                    c4.y += 5 * -0.50
                elif 120 <= c4.y <= 370:
                    c4.carStartImgAndRotate2(Background.screen)
                    c4.x += 5 * 0.4
                    c4.y -= 5 * 0.6


            # Put Ped on the road (For demo)

            # Put pedestrian on the road
            if random.randint(0, int(pedGenRate / simulatorSpeed * 5)) == 1:
                line = random.randint(0, 3)
                pedStartNum = random.randint(0, 1)

                c = Pedestrian(Background.pedStart0XAry[line], Background.pedStart0YAry[pedStartNum],
                               random.uniform(0.2, 0.4) * simulatorSpeed, 0, line, pedStartNum)
                pedArray.append(c)
            # Put Grand mother on the road
            if random.randint(0, int(grandMotherGenRate / simulatorSpeed)) == 1: # Put Grandmother on the road
                line = random.randint(0, 3)
                pedStartNum = random.randint(0, 1)

                c = Pedestrian(Background.pedStart0XAry[line], Background.pedStart0YAry[pedStartNum],
                               random.uniform(0.09, 0.1) * simulatorSpeed, 0, line, pedStartNum)
                pedArray.append(c)

            for p in pedArray:
                # pedStart0 to pedStart1
                if p.y >= Background.pedStart0YAry[1] and p.pedStartNum == 0:
                    p.pedStart(Background.screen, Color.lightBlue)
                    # Check Traffic light
                    if pedLight == "red" and p.y == Background.pedStart0YAry[0]:
                        p.y -= 0
                        p.waitingTime += 1 * simulatorSpeed
                    elif pedLight == "green" or p.y != Background.pedStart0YAry[0]:
                        p.y -= p.speed

                # pedStart1 to pedStart0
                if p.y <= Background.pedStart0YAry[0] and p.pedStartNum == 1:
                    p.pedStart(Background.screen, Color.lightBlue)
                    # Check Traffic light
                    if pedLight == "red" and p.y == Background.pedStart0YAry[1]:
                        p.y += 0
                        p.waitingTime += 1 * simulatorSpeed
                    elif pedLight == "green" or p.y != Background.pedStart0YAry[1]:
                        p.y += p.speed

            # Print pedestrian number
            for ped in pedArray:
                if ped.y == Background.pedStart0YAry[0] and ped.pedStartNum == 0:
                    Background.pedStart[0] += 1
                if ped.y == Background.pedStart0YAry[1] and ped.pedStartNum == 1:
                    Background.pedStart[1] += 1

            sys_font = pygame.font.SysFont("None", 16)

            rendered = sys_font.render(str(Background.pedStart[0]), 0, (35, 20, 245))
            Background.screen.blit(rendered, (Background.res_x * 0.335, Background.res_y * 0.71))

            rendered = sys_font.render(str(Background.pedStart[1]), 0, (35, 20, 245))
            Background.screen.blit(rendered, (Background.res_x * 0.335, Background.res_y * 0.546))

            rendered = sys_font.render(str(Background.pedStart[2]), 0, (35, 20, 245))
            Background.screen.blit(rendered, (Background.res_x * 0.34, Background.res_y * 0.505))

            Background.pedStart[0] = 0
            Background.pedStart[1] = 0

            sys_font = pygame.font.SysFont("None", 16)
            rendered = sys_font.render("Pedestrain waiting time at junction counter(for ITLS switching): " + str(round(pedWaitingtimeAtJunction, 2)), 0, (0, 0, 0))
            Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.83))

            sys_font = pygame.font.SysFont("None", 16)
            rendered = sys_font.render("Car waiting time at junction counter(for ITLS switching): " + str(round(carWaitingtimeAtJunction, 2)), 0, (0, 0, 0))
            Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.85))

            sys_font = pygame.font.SysFont("None", 16)
            rendered = sys_font.render( "carlight status: " + carLight, 0, (0, 0, 0))
            Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.87))

            rendered = sys_font.render("pedlight status: " + pedLight, 0, (0, 0, 0))
            Background.screen.blit(rendered, (Background.res_x * 0.51, Background.res_y * 0.89))

            rendered = sys_font.render("pervious carlight time: " + str(carLightChgTime), 0, (0, 0, 0))
            Background.screen.blit(rendered, (Background.res_x * 0.7, Background.res_y * 0.87))

            rendered = sys_font.render("pervious pedlight time: " + str(pedLightChgTime), 0, (0, 0, 0))
            Background.screen.blit(rendered, (Background.res_x * 0.7, Background.res_y * 0.89))

            # Update Game
            clock.tick(30)
            pygame.display.update()
    # Print Simulation data
    print()
    print("Simulation has run for " + str(time.time() - simStartTime) + " second(s) real time")

    print("Simulation has run for " + str(simTime) + " second(s) simulating time")
    print(str(frameCount) + " of frames has pass ")

    print("Total car number on the street: " + str(len(carArray)))
    for car in carArray:
        totalCarWaitingTime += car.waitingTime
    print("Average car watiting time: " + str(totalCarWaitingTime / len(carArray) / 30) + " seconds")

    print("Total pedestrian number on the street: " + str(len(pedArray)))
    for ped in pedArray:
        totalPedWaitingTime += ped.waitingTime
    print("Average pedestrian watiting time: " + str(totalPedWaitingTime / len(carArray) / 30) + " seconds")

    # Save data to file

    book = openpyxl.load_workbook('result.xlsx')
    sheet = book.active

    # K1 default = 1
    countSave = sheet['U1']
    countSave.value += 1

    sheet['U1'] = countSave.value
    sheet[str('A' + str(countSave.value))] = countSave.value - 1
    sheet[str('B' + str(countSave.value))] = simTime
    sheet[str('C' + str(countSave.value))] = len(carArray)
    sheet[str('D' + str(countSave.value))] = len(pedArray)
    sheet[str('E' + str(countSave.value))] = totalCarWaitingTime / len(carArray) / 30
    sheet[str('F' + str(countSave.value))] = totalPedWaitingTime / len(pedArray) / 30

    sheet[str('G' + str(countSave.value))] = carMaxNumAtJunction # Max number of car wait at junction
    sheet[str('H' + str(countSave.value))] = carMaxWaitingtimeAtJunction # Switch light if a car wait more than x sec (Must Be > 16)
    sheet[str('I' + str(countSave.value))] = carLightGreenMinTime  #The least Carlight Green time last

    sheet[str('J' + str(countSave.value))] = pedMaxNumAtJunction # Max number of pedstrain wait at junction
    sheet[str('K' + str(countSave.value))] = pedMaxWaitingtimeAtJunction # Switch light if a ped wait more than x sec
    sheet[str('L' + str(countSave.value))] = pedLightGreenMinTime #The least Carlight Green time last

    sheet[str('M' + str(countSave.value))] = pedLightFlashLongerTime # Exetend Flashing Green Time for pedLight

    book.save("result2.xlsx")


if __name__ == "__main__":
    index = 0

    for i in range(1):
        try:
            x = threading.Thread(target=main_sim(random.randint(5, 15), random.randint(5, 20), random.randint(5, 60), random.randint(5, 20), random.randint(5, 20), random.randint(5, 60), random.randint(3, 10)), args=(index,))
            # x = threading.Thread(target=main_sim(7, 22, 6, 17, 16, 10, 5), args=(index,))

              #  1 = 5, 15  carMaxNumAtJunction
              #  2 = 5 , 20 carLightGreenMinTime
              #  3 = 5 , 60 carMaxWaitingtimeAtJunction

              #  4 = 5, 20  pedMaxNumAtJunction
              #  5 = 5 , 20 pedLightGreenMinTime
              #  6 = 5, 60  pedMaxWaitingtimeAtJunction

              #  7 = 3 , 10 pedLightFlashLongerTime
            x.start()
            x.join()
            index += 1
            print("the no " +  str(i) + "'s sim")
        except Exception as e:
            print("Error: unable to start Simulation. Reason:")
            print(e)