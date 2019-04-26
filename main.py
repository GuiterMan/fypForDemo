import pygame
import random
import time
import openpyxl
from background import Background
from color import Color
from car import Car
from pedestrian import Pedestrian
from checkCollision import isTooCloseToCarInFront, isCarCollided, pedLightIsWalking
from carLight import carTrafficLightSignalSwitching
from pedLight import pedTrafficLightSignalSwitching

pygame.init()

# Set Simulator changeable variable
itlsMode = True  # Use ITLS mode or Normal Light
simulatorSpeed = 3  # Simulator speed (default = 1)
totalCarNum = 2500  # How many car generate in the sim period
totalPedNum = 2000  # How many pedestrian generate in the sim period
totalGrandMotherNum = 12 # How many grandmother generate in the sim period
simTimePeriod = 3600  # How long the simulation run (in sec)

carGenRate = (simTimePeriod * 30) / totalCarNum  # sec * frames / total carNum
pedGenRate = (simTimePeriod * 30) / totalPedNum  # sec * frames / total carNum
grandMotherGenRate = (simTimePeriod * 30) / totalGrandMotherNum
pedMaxNumAtJunction = 20  # Max number of pedstrain wait at junction
carMaxNumAtJunction = 15 # Max number of pedstrain wait at junction
carLightGreenMaxTime = simTimePeriod  # Car green light max time
carLightGreenMinTime = 10 #The least Carlight Green time last
pedLightGreenMaxTime = simTimePeriod  # Car green light max time
pedLightGreenMinTime = 10 #The least Carlight Green time last
carLightRedMaxTime = 24  # Car red light max time (Must Be > 16)
pedLightFlashLongerTime = 5 # Exetend Flashing Green Time for pedLight
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

            if (countPedWaitAtJunctionTime == False) and ((pedLight == "red") or (pedLight == "flashingGreen")):
                pedWaitingtimeAtJunction = simTime - pedWaitingtimeAtJunctionTimeStamp
            else:
                pedWaitingtimeAtJunction = 0

            if (carLight == "green" and
                    (((simTime - carLightChgTime >= carLightGreenMinTime) and ((pedCountAtPedStart >= pedMaxNumAtJunction) or (pedWaitingtimeAtJunction > 30))) or (simTime - carLightChgTime >= carLightGreenMaxTime))):  # CarLight switch to red conditiion
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
                (((simTime - pedLightChgTime >= carLightGreenMinTime) and ((carCountAtCarLight >= carMaxNumAtJunction) or (carWaitingtimeAtJunction > 30))) or (simTime - pedLightChgTime >= pedLightGreenMaxTime))):  # CarLight switch to red conditiion

                pedLight = "flashingGreen"
                countPedWaitAtJunctionTime = True
                countPedLightTime = True

            elif pedLight == "flashingGreen" and simTime - pedLightChgTime > 10:
                if pedLightIsWalking(pedArray, Background.pedStart0YAry):
                    pedLight == "flashingGreenLonger"
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
        if random.randint(0, int(carGenRate / simulatorSpeed)) == 1:
            line = random.randint(0, 3)
            c = Car(Background.res_x - 100, Background.yArray[line], random.uniform(2, 4) * simulatorSpeed, 0,
                    line)  # The place that car start
            carArray.append(c)
            carLineArray.append([line, c])

        for c in carArray:
            if c.x > 100:  # The place that car out
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
                elif 588 > c.x > 387:
                    c.x -= c.speed * 0.97  # slope of cars
                    c.y += c.speed * 0.03
                # Check 3rd part carlight junction movement
                elif 393 >= c.x > 377:
                    if carLight == "green":
                        if pedLightIsWalking(pedArray, Background.pedStart0YAry):
                            c.x -= 0
                            c.waitingTime += 1 * simulatorSpeed
                        else:
                            c.x -= c.speed * 0.97
                            c.y += c.speed * 0.03
                    elif carLight == "greenToYellow" or carLight == "redToYellow":
                        if c.x >= 377:
                            c.x -= 0
                            c.waitingTime += 1 * simulatorSpeed
                        else:
                            c.x -= c.speed * 0.97
                            c.y += c.speed * 0.03
                    elif carLight == "red":
                        c.x -= 0
                        c.waitingTime += 1 * simulatorSpeed
                # 4rd part Route movement
                elif 377 >= c.x > 100:
                    c.x -= c.speed * 0.91
                    c.y += c.speed * 0.09

        # Put pedestrian on the road
        if random.randint(0, int(pedGenRate / simulatorSpeed)) == 1:
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
                           random.uniform(0.09, 0.09) * simulatorSpeed, 0, line, pedStartNum)
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

        rendered = sys_font.render("pervious pedlight time: " + str(carLightChgTime), 0, (0, 0, 0))
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
countSave = sheet['K1']
countSave.value += 1

sheet['K1'] = countSave.value
sheet[str('A' + str(countSave.value))] = countSave.value - 1
sheet[str('B' + str(countSave.value))] = simTime
sheet[str('C' + str(countSave.value))] = len(carArray)
sheet[str('D' + str(countSave.value))] = len(pedArray)
sheet[str('E' + str(countSave.value))] = totalCarWaitingTime / len(carArray) / 30
sheet[str('F' + str(countSave.value))] = totalPedWaitingTime / len(pedArray) / 30

book.save("result.xlsx")
