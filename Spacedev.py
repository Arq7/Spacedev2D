# =============== 2D Commandline Engine =============== #
# Ver 0.07
# Fixed and improved rendering (updates)
# Simple generation of obstacles
# ...And walls around the area
# Simple AI pathfinding
# Simplified movement function
# ...and added support for single tile movement
# Changed input handling (releasing control)
# Debug mode

# Todo:
# Add multiple moves in one turn
# Finish collisions
# Replay system
# Maybe Rework instance system
#
# Possibly a sprite bank system

# Bug 1: x, y are flipped
# Bug 2: 
# =============== --------------------- =============== #

import time
import sys
import os
import random

# =============== Sprites =============== #

s_empty = "."
s_missile = "o"
s_up = 'A'
s_down = 'V'
s_right = '>'
s_left = '<'
s_wall = '+'
s_target = 'Q'
s_ai = '$'

# =============== Classes =============== #


class Object:
    # class variable
    object_count = 0

    def __init__(self, x, y, sprite, xspeed=0, yspeed=0, rotation='up'):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.rotation = rotation

        Object.object_count += 1

# =============== Initiation =============== #

#               Fields:
OBJECTS = []    # Requires input
MISSILES = []   # Missiles
FIELD_3 = []    # Stable and invincible
AIS = []        # Runs AI logic
TARGETS = []    # Moving in the background

FIELDS = [OBJECTS, MISSILES, FIELD_3, TARGETS, AIS]

# Init some ships:
#               x, y, sprite, x&y spd, rotation
e_ship = Object(4, 4, s_down, 0, 0, 'down')
p_ship = Object(35, 25, s_up, 0, 0, 'up')

# Map
MAP_H = 80 # W of map
MAP_W = 40 # H of map
# Create map
MAP = [[s_empty] * MAP_W for i in range(MAP_H)]

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
    for alist in FIELDS:
        for obj in alist:
            MAP[obj.x][obj.y] = obj.sprite

def update_map(com=0):
    """MAP TOOL: 0 = update
                 1 = update and print"""
    
    erase_map()
    seton_map()
    if com == 1:
        time.sleep(0.1)
        os.system('cls')
        print_map()
        

# Calculations
def move_object(ship, anim = 0, debug = 0):
    """Movement function"""

    move = True
    xdirection = 0
    ydirection = 0

    moves = abs(ship.xspeed) + abs(ship.yspeed)
    if debug == 1:
        print('In the move function of', ship.sprite, 'at', ship.x,'x', ship.y)
        print('moves=', moves)

    if moves != 0:
        xmoves = abs(ship.xspeed)
        ymoves = abs(ship.yspeed)

        if ship.xspeed > 0: xdirection = 1
        elif ship.xspeed < 0: xdirection = -1
        if ship.yspeed > 0: ydirection = 1
        elif ship.yspeed < 0: ydirection = -1
        
        if debug == 1:
            print('xdirection=', xdirection)
            print('ydirection=', ydirection)
            print('xspeed=', ship.xspeed)
            print('yspeed=', ship.yspeed)
            print('xmoves=', xmoves)
            print('ymoves=', ymoves)

        while move is True:

            # -X- MOVEMENT
            if xmoves > 0:
                    
                else: # Proper move

                    update_map()
                    print(xmoves, 'xmoves left')

            # -Y- MOVEMENT
            if ymoves > 0:
                if MAP[ship.x][ship.y+ydirection] != s_empty: # Collision
                    ship.yspeed = 0
                    xmoves = 0
                    ymoves = 0
                    # Collision damage
                    col = find_obj(ship.x, ship.y+ydirection)
                    print('Found:', col, 'at', col.x, col.y)
                    print('Crash with', MAP[ship.x][ship.y+ydirection], 'in direction', ydirection)
                    destroy_obj(col)
                    destroy_obj(ship)

                    update_map()
                xmoves, ymoves = col_move(ship, 0, ydirection, xmoves, ymoves, anim)
                

            if xmoves + ymoves == 0:
                move = False

            if ship.x >= MAP_H - 1 or ship.x <= 0 or ship.y >= MAP_W - 1 or ship.y <= 0:
                # Map border ! MAP_H cuz it's flipped :\
                ship.xspeed = 0
                ship.yspeed = 0
                xmoves = 0
                ymoves = 0
                destroy_obj(ship)
                if debug == 1:
                    print('Map ends')
                update_map()

                
    if debug == 1:
        print('Movement completed for', ship.sprite, '\n')

def col_move(ship, xdirection, ydirection, xmoves, ymoves, anim=0, debug=0):

    if MAP[ship.x+xdirection][ship.y+ydirection] != s_empty: # Collision
        ship.yspeed = 0
        ship.xspeed = 0
        xmoves = 0
        ymoves = 0
        
        # Collision handling
        col = find_obj(ship.x+xdirection, ship.y+ydirection)

        if debug == 1:
            print('Found:', col, 'at', col.x, col.y)
            print('Crash with', MAP[ship.x+xdirection][ship.y+ydirection])

        # Collision logic - improve
        if ship in AIS:
            pass
        elif col in FIELD_3:
            if ship in MISSILES:
                destroy_obj(ship)    
        else:  
            destroy_obj(col)
            destroy_obj(ship)

        update_map(anim)

    else: # Proper move
        if debug == 1:
            print('Moving to', MAP[ship.x+xdirection][ship.y+ydirection])
            
        ship.y += ydirection
        ship.x += xdirection
        if xdirection == 0:
            ymoves -= 1
        if ydirection == 0:
            xmoves -= 1
        update_map(anim)
        
        if debug == 1:
            print(xmoves, 'xmoves left')

    return xmoves, ymoves


def fire(ship):
    if ship.rotation == 'up':
        if MAP[ship.x][ship.y-1] == s_empty:
            obj = Object(ship.x,ship.y-1,s_missile,0,-missile_speed)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'down':
        if MAP[ship.x][ship.y+1] == s_empty:
            obj = Object(ship.x,ship.y+1,s_missile,0,missile_speed)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'right':
        if MAP[ship.x+1][ship.y] == s_empty:
            obj = Object(ship.x+1,ship.y,s_missile,missile_speed,0)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'left':
        if MAP[ship.x-1][ship.y] == s_empty:
            obj = Object(ship.x-1,ship.y,s_missile,-missile_speed,0)
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

def move_field(FIELD, arg1=0, arg2=0):
    """Moves all objects in the field"""
    COPY = FIELD[:] #.copy()
    for obj in COPY:
        if obj in FIELD:
            move_object(obj, arg1, arg2)


def generate_obstacles(num):
    for i in range(num):
        randx= random.randrange(1, MAP_H)
        randy= random.randrange(1, MAP_W)
        if MAP[randx][randy] == s_empty:
            obs = Object(randx,randy, s_wall)
            FIELD_3.append(obs)

def generate_ai(num):
    for i in range(num):
        randx= random.randrange(1, MAP_H)
        randy= random.randrange(1, MAP_W)
        if MAP[randx][randy] == s_empty:
            obs = Object(randx,randy, s_ai)
            AIS.append(obs)

def generate_target(num):
    for i in range(num):
        while True:
            randx= random.randrange(1, MAP_H-1)
            randy= random.randrange(1, MAP_W-1)
            randsx= random.randrange(-1, 2)
            randsy= random.randrange(-1, 2)
            if MAP[randx][randy] == s_empty:
                obs = Object(randx,randy, s_target, randsx, randsy)
                TARGETS.append(obs)
                break
            
def generate_border():
    for i in range(MAP_H):
        if MAP[i][0] == s_empty:
            obs = Object(i,0, s_wall)
            FIELD_3.append(obs)
    for i in range(MAP_H):
        if MAP[i][MAP_W-1] == s_empty:
            obs = Object(i,MAP_W-1, s_wall)
            FIELD_3.append(obs)
    for i in range(MAP_W):
        if MAP[MAP_H-1][i] == s_empty:
            obs = Object(MAP_H-1, i, s_wall)
            FIELD_3.append(obs)
    for i in range(MAP_W):
        if MAP[0][i] == s_empty:
            obs = Object(0, i, s_wall)
            FIELD_3.append(obs)
# =============== MAIN LOOP =============== #

missile_speed = 7

handling = True
turn = True

generate_border()
generate_obstacles(40)
#generate_target(20)
generate_ai(30)

OBJECTS.append(p_ship)
#OBJECTS.append(e_ship)

while True:

    #print('--------Turn starts----------')

    
    update_map(1)

    # Input handling
    turn = True
    
    while turn == True and handling == True:
        for ship in OBJECTS:

            # 1 distance movement
            ship.xspeed = 0
            ship.yspeed = 0
            
            print(handling)
            print('Make a move for', ship.sprite)
            inp = input('Input (w/s/a/d, f, h, i/k/j/l, b, x): ')

            # Move
            if inp == 'a':
                ship.xspeed -= 1
                turn = False
            elif inp == 'd':
                ship.xspeed += 1
                turn = False
            elif inp == 'w':
                ship.yspeed -= 1
                turn = False
            elif inp == 's':
                ship.yspeed += 1
                turn = False
            # Skip movement    
            elif inp == 'h':
                turn = False
                handling = False
            # Exit
            elif inp == 'x':
                sys.exit()
            # Break
            elif inp == 'b':
                ship.yspeed = 0
                ship.xspeed = 0
                print('Breaking...')
                turn = False
            # Fire
            elif inp == 'f':
                fire(ship)
                turn = False
            # Rotation
            elif inp == 'i':
                ship.rotation = 'up'
                ship.sprite = s_up
                update_map(1)
            elif inp == 'k':
                ship.rotation = 'down'
                ship.sprite = s_down
                update_map(1)
            elif inp == 'j':
                ship.rotation = 'left'
                ship.sprite = s_left
                update_map(1)
            elif inp == 'l':
                ship.rotation = 'right'
                ship.sprite = s_right
                update_map(1)
            elif inp == '' or ' ':
                turn = False    
            # No inputs afterwards

    for ai in AIS:
        if len(OBJECTS) == 0:
            ai.xspeed = random.randrange(-1, 2)
            ai.yspeed = random.randrange(-1, 2)
        else:
            target = OBJECTS[0]
            # Simple path
##            if target.x == ai.x:
##                ai.xspeed = 0
##            if target.y == ai.y:
##                ai.yspeed = 0
            if target.x > ai.x:
                ai.xspeed = 1
            if target.x < ai.x:
                ai.xspeed = -1
            if target.y > ai.y:
                ai.yspeed = 1
            if target.y < ai.y:
                ai.yspeed = -1

    move_field(MISSILES, 1)
    move_field(OBJECTS, 1)
    move_field(TARGETS)
    move_field(AIS)

    if len(OBJECTS) == 0 and len(TARGETS) == 0 and len(AIS) == 0:
        print('No more objects on the map')
        break
    
    #print('----------Turn ends----------')

input('Press to exit')


