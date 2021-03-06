# check tooCloseToCarInFront
def isTooCloseToCarInFront(carLineArray, c):
    for row in carLineArray:
        if row[0] == c.line:
            if 50 > (c.x - row[1].x) > 0:
              return True
    return False

# check collision 4line
def isCarCollided(carLineArray, c):
    for row in carLineArray:
        if row[0] == c.line:
            if 35 > (c.x - row[1].x) > 0:
                return True
            elif row[2] and 60 > c.x - row[1].x > 0:
                return True
    return False

# check collision left road
def line56IsCarCollided(carLineArray, c):
    for row in carLineArray:
        if row[0] == c.line:
            if 40 > (c.x - row[1].x) > 0 and 5 > c.y - row[1].y > -5:
              return True
    return False


def pedLightIsWalking(pedArray, pedStart0YAry):
    for ped in pedArray:
        if ped.y <= pedStart0YAry[0] and ped.pedStartNum == 1 and ped.y != pedStart0YAry[1]:
            return True
        if ped.y >= pedStart0YAry[1] and ped.pedStartNum == 0 and ped.y != pedStart0YAry[0]:
            return True
    return False
