# =============== Fleet Combat Test =============== #
# Ver 0.05
# - Added collisions
# - Reworked lists of objects (fields)
# - Added find functionality

# Todo:
# Add asteroids for some fun
# Collision masks?
# Rework instance system
#
# Possibly a sprite sheet?

# Bug 1: x, y are flipped
# Bug 2: move near the border is not perfect

# =============== ----------------- =============== #

import time

# =============== Sprites =============== #

s_empty = "."
s_missile = "o"
s_up = 'A'
s_down = 'V'
s_right = '>'
s_left = '<'
s_asteroid = 'G'

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

# Fields
OBJECTS = []
MISSILES = []
FIELDS = [OBJECTS, MISSILES]

# Init some ships:
#               x, y, sprite, x&y spd, rotation

e_ship = Object(4, 4, s_down, 0, 0, 'down')
p_ship = Object(4, 15, s_up, 0, 0, 'up')

OBJECTS.append(p_ship)
OBJECTS.append(e_ship)

# Map
MAP_H = 40 # W of map
MAP_W = 26 # H of map

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
                    print('Map ends')
                    destroy_obj(ship)
                elif MAP[ship.x+xdirection][ship.y] != s_empty: # Collision
                    ship.xspeed = 0
                    xmoves = 0
                    ymoves = 0
                    # Collision damage
                    col = find_obj(ship.x+xdirection, ship.y)
                    print('Found:', col, 'at', col.x, col.y)
                    print('Crash with', MAP[ship.x+xdirection][ship.y], 'in direction', xdirection)
                    destroy_obj(col)
                    destroy_obj(ship)
                    erase_map()
                    seton_map()
                    
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
                    print('Map ends')
                    destroy_obj(ship)
                elif MAP[ship.x][ship.y+ydirection] != s_empty: # Collision
                    ship.yspeed = 0
                    xmoves = 0
                    ymoves = 0
                    # Collision damage
                    col = find_obj(ship.x, ship.y+ydirection)
                    print('Found:', col, 'at', col.x, col.y)
                    print('Crash with', MAP[ship.x][ship.y+ydirection], 'in direction', ydirection)
                    destroy_obj(col)
                    destroy_obj(ship)
                    erase_map()
                    seton_map()
                    
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


def fire(ship):
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
    "Removes an obj from its field"
    for alist in FIELDS:
        for i in alist:
            if i == obj:
                MAP[obj.x][obj.y] = s_empty
                alist.remove(obj)

def find_obj(x,y):
    """Returns the object"""
    for alist in FIELDS:
        for obj in alist:
            if x == obj.x and obj.y == y:
                return(obj)


# =============== MAIN LOOP =============== #

while True:

    print('--------Turn starts----------')


        
    erase_map()
    seton_map()
    print_map()
    time.sleep(0.1)

    # Input handling
    for ship in OBJECTS:
        print('Make a move for', ship.sprite)
        inp = input('Input (w/s/a/d, f, b, i/k/j/l): ')
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

        cMISSILES = MISSILES[:] # Same as .copy()
    for missile in cMISSILES:
        move_object(missile)

    for ship in OBJECTS:
        move_object(ship)
        

    erase_map()
    seton_map()
    print_map()

    if len(OBJECTS) == 0:
        print('No more objects')
        break

    print('----------Turn ends----------')

input('Press to exit')


