# =============== Fleet Combat Test =============== #
# Ver 0.04
# - Added support for multiple ships
# - Added full movement options and basic rotation

# Todo:
# Add asteroids for some fun
# Add collisions, maybe layers and collision masks
# Rework instance system

# Bug 1: x, y are flipped
# Bug 2: move near the border is not perfect

# =============== ----------------- =============== #

import time

# Sprites

s_empty = "."
# s_p_ship = "P"
# s_e_ship = "X"
s_missile = "o"
s_up = 'A'
s_down = 'V'
s_right = '>'
s_left = '<'

# =============== Classes =============== #


class Object:
    # class variable
    object_count = 0

    def __init__(self, x, y, sprite, xspeed, yspeed, rotation='up'):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.rotation = rotation

        Object.object_count += 1

# class Missile(Object): INCLUDE MISSILE OBJECT

# =============== Initiation =============== #

# Init some ships:
#               x, y, sprite,  x&y spd, rotation
e_ship = Object(3, 4, s_down, 0, 0, 'down')
p_ship = Object(5, 15, s_up, 0, 0, 'up')

OBJECTS = [p_ship, e_ship]
MISSILES = []

# Map
MAP_H = 10 # W w praktyce
MAP_W = 20 # H w praktyce

MAP = [[s_empty] * MAP_W for i in range(MAP_H)]
# print(MAP)

# =============== Functions =============== #

# Map-related
def print_map():
    """Prints the MAP"""
    print('')
    for y in range(MAP_W):
        print('|', end=' ')
        for x in range(MAP_H):
            print(MAP[x][y], end=' ')
        print('|')
    print('')


def erase_map():
    """Clean the MAP before rendering"""
    for i in range(MAP_W):
        for j in range(MAP_H):
            MAP[j][i] = s_empty


def seton_map():
    """Set objects on the MAP based on their x, y coordinates"""
    for object in OBJECTS:
        MAP[object.x][object.y] = object.sprite
    for object in MISSILES:
        MAP[object.x][object.y] = object.sprite


# Calculations
def move_object(ship):
    """Movement function"""

    print('In the move function of', ship.sprite, 'at', ship.x,'x', ship.y)

    move = True
    xdirection = 0
    ydirection = 0

    moves = abs(ship.xspeed) + abs(ship.yspeed)
    print('moves=', moves)

    if moves != 0:
        xmoves = abs(ship.xspeed)
        ymoves = abs(ship.yspeed)
        print('xspeed=', ship.xspeed)
        print('yspeed=', ship.yspeed)
        print('xmoves=', xmoves)
        print('ymoves=', ymoves)

        if ship.xspeed > 0: xdirection = 1
        elif ship.xspeed < 0: xdirection = -1
        if ship.yspeed > 0: ydirection = 1
        elif ship.yspeed < 0: ydirection = -1

        print('xdirection=', xdirection)
        print('ydirection=', ydirection)

        while move is True:

            # -X- MOVEMENT
            if xmoves > 0:
                if ship.x >= MAP_H - 1 or ship.x <= 0: # Map border ! MAP_H cuz it's flipped :\
                    ship.xspeed = 0
                    ship.yspeed = 0
                    xmoves = 0
                    ymoves = 0
                    erase_map()
                    seton_map()
                    print('Granica')
                    destroy_obj(ship)
                elif MAP[ship.x+xdirection][ship.y] != s_empty: # Collision
                    ship.xspeed = 0
                    xmoves = 0
                    ymoves = 0
                    # Collision damage
                    erase_map()
                    seton_map()
                    print('Crash with', MAP[ship.x+xdirection][ship.y], 'in direction', xdirection)
                else: # Proper move
                    print('Moving to', MAP[ship.x+xdirection][ship.y], 'in the direction of x', xdirection)
                    ship.x += xdirection
                    erase_map()
                    seton_map()
                    print_map()
                    time.sleep(0.1)
                    xmoves -= 1
                    print(xmoves, 'xmoves left')

            # -Y- MOVEMENT
            if ymoves > 0:
                if ship.y >= MAP_W - 1 or ship.y <= 0: # Map border
                    ship.yspeed = 0
                    ship.xspeed = 0
                    xmoves = 0
                    ymoves = 0
                    erase_map()
                    seton_map()
                    print('Granica')
                    destroy_obj(ship)
                elif MAP[ship.x][ship.y+ydirection] != s_empty: # Collision
                    ship.yspeed = 0
                    xmoves = 0
                    ymoves = 0
                    # Collision damage
                    # destroy_obj(ship) Nie tak suabo :v
                    erase_map()
                    seton_map()
                    print('Crash with', MAP[ship.x][ship.y+ydirection], 'in direction', ydirection)
                else:  # Proper move
                    print('Moving to', MAP[ship.x][ship.y+ydirection], 'in the direction of y', ydirection)
                    ship.y += ydirection
                    erase_map()
                    seton_map()
                    print_map()
                    time.sleep(0.1)
                    ymoves -= 1
                    print(ymoves, 'ymoves left')

            if xmoves + ymoves == 0:
                print('Move = False')
                move = False

    print('Movement completed for', ship.sprite, '\n')


def fire(ship): # Do more directions
    if ship.rotation == 'up':
        if MAP[ship.x][ship.y-1] == s_empty:
            obj = Object(ship.x,ship.y-1,s_missile,0,-6)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'down':
        if MAP[ship.x][ship.y+1] == s_empty:
            obj = Object(ship.x,ship.y+1,s_missile,0,6)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'right':
        if MAP[ship.x+1][ship.y] == s_empty:
            obj = Object(ship.x+1,ship.y,s_missile,6,0)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'left':
        if MAP[ship.x-1][ship.y] == s_empty:
            obj = Object(ship.x-1,ship.y,s_missile,-6,0)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")


def destroy_obj(obj):
    if obj in OBJECTS:
        OBJECTS.remove(obj)
    elif obj in MISSILES:
        MISSILES.remove(obj)
    MAP[obj.x][obj.y] = s_empty


# =============== MAIN LOOP =============== #
while True:

    print('--------Turn starts----------')
    erase_map()
    seton_map()
    print_map()
    time.sleep(0.1)

    for ship in OBJECTS:
        print('Make a move for', ship.sprite)
        inp = input('Input: ')
        if inp == 'a':
            ship.xspeed -= 1
        elif inp == 'd':
            ship.xspeed += 1
        elif inp == 'w':
            ship.yspeed -= 1
        elif inp == 's':
            ship.yspeed += 1
        elif inp == 'b':
            ship.yspeed = 0
            ship.xspeed = 0
            print('Breaking...')
            print(ship.xspeed, ship.yspeed)
        # Fire
        elif inp == 'f':
            fire(ship)
        # Rotation
        elif inp == 'i':
            ship.rotation = 'up'
            ship.sprite = s_up
        elif inp == 'k':
            ship.rotation = 'down'
            ship.sprite = s_down
        elif inp == 'j':
            ship.rotation = 'left'
            ship.sprite = s_left
        elif inp == 'l':
            ship.rotation = 'right'
            ship.sprite = s_right

        print(ship.rotation)

    for ship in OBJECTS:
        move_object(ship)
    for missile in MISSILES:
        move_object(missile)

    erase_map()
    seton_map()
    print_map()

    if len(OBJECTS) == 0:
        print('No more objects')
        break

    # ext = input('----------Turn ends----------')
    print('----------Turn ends----------')