# =============== 2D Commandline Engine =============== #
# Ver 0.08.1
# Fixed X and Y on the MAP

# Todo:
# Maybe Rework instance system
#
# Possibly a sprite bank system

# Bug 1: Some functions don't work without borders
# Infitite loop while player colides
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
s_wall = 'X'
s_target = 'Q'
s_ai = '$'
s_small = 's'
s_predator = 'P'


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
        self.birth_rate = 3
        self.age = 0
        self.missile_speed = 15
        self.birth_age = 14

        Object.object_count += 1


# =============== Initiation =============== #

#               Fields:
OBJECTS = []  # Requires input
MISSILES = []  # Missiles
WALLS = []  # Stable and invincible
AIS = []  # Runs AI logic
TARGETS = []  # Moving in the background
PREY = []
PREDATORS = []

FIELDS = [OBJECTS, MISSILES, WALLS, TARGETS, AIS, PREY, PREDATORS]

# Init some ships:
#               x, y, sprite, x&y spd, rotation
e_ship = Object(4, 4, s_down, 0, 0, 'down')
p_ship = Object(35, 25, s_up, 0, 0, 'up')

# Map
MAP_H = 35  # W of map
MAP_W = 65  # H of map
# Create map
#MAP = [[s_empty] * MAP_W for i in range(MAP_H)]

MAP = []
for x in range(MAP_W): # The main list is a list of 60 lists.
    MAP.append([])
    for y in range(MAP_H):
        MAP[x].append(s_empty)


# =============== Functions =============== #

# Map-related
def print_map():
    """Prints the MAP"""
    print('')
    for y in range(MAP_H):
        print('|', end=' ')
        for x in range(MAP_W):
            print(MAP[x][y], end=' ')
        print('|')
    print('')


def erase_map():
    """Clean the MAP before rendering"""
    for i in range(MAP_H):
        for j in range(MAP_W):
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
        time.sleep(0.01)
        os.system('cls')
        print_map()


# Calculations
def move_object(ship, anim=0, debug=0):
    """Movement function. Moves each object based on their speed.
    If xspeed == 1 object moves one tile. Else, it moves more than once.
    Each move is calculated and checked for a collision.
    x and y directions are created based on xspeed and yspeed."""

    if abs(ship.xspeed) + abs(ship.yspeed) == 0:
        return

    if debug == 1:
        print('In the move function of', ship.sprite, 'at', ship.x, 'x', ship.y)
        print('moves=', moves)

    xdirection = 0
    ydirection = 0
    xmoves = abs(ship.xspeed)
    ymoves = abs(ship.yspeed)

    if ship.xspeed > 0:
        xdirection = 1
    elif ship.xspeed < 0:
        xdirection = -1
    if ship.yspeed > 0:
        ydirection = 1
    elif ship.yspeed < 0:
        ydirection = -1

    if debug == 1:
        print('xdirection=', xdirection)
        print('ydirection=', ydirection)
        print('xspeed=', ship.xspeed)
        print('yspeed=', ship.yspeed)
        print('xmoves=', xmoves)
        print('ymoves=', ymoves)

    while True:
        if xmoves > 0:  # -X- MOVEMENT
            xmoves, ymoves = col_move(ship, xdirection, 0, xmoves, ymoves, anim)
        if ymoves > 0:  # -Y- MOVEMENT
            xmoves, ymoves = col_move(ship, 0, ydirection, xmoves, ymoves, anim)
        if xmoves + ymoves == 0:
            break
        if ship.x >= MAP_W - 1 or ship.x <= 0 or ship.y >= MAP_H - 1 or ship.y <= 0:
            ship.xspeed = 0
            ship.yspeed = 0
            xmoves = 0
            ymoves = 0
            destroy_obj(ship)
            if debug == 1:
                print('Map ends')
            # update_map()
    if debug == 1:
        print('Movement completed for', ship.sprite, '\n')


def col_move(ship, xdirection, ydirection, xmoves, ymoves, anim=0, debug=0):
    """Only modifies xmoves and ymoves for the move function,
    but also can destroy objects and modify object data"""

    if MAP[ship.x + xdirection][ship.y + ydirection] != s_empty:  # Collision
        ship.yspeed = 0
        ship.xspeed = 0
        xmoves = 0
        ymoves = 0

        # Collision handling
        col = find_obj(ship.x + xdirection, ship.y + ydirection)

        if debug == 1:
            print('Found:', col, 'at', col.x, col.y)
            print('Crash with', MAP[ship.x + xdirection][ship.y + ydirection])

        # Collision logic - improve

        if col in WALLS:
            if ship in MISSILES:
                destroy_obj(ship)
        elif ship in PREY:  # Prey logic
            if col in PREY:
                create_child(ship, col, PREY)
            elif col in PREDATORS:
                destroy_obj(ship)
        elif ship in PREDATORS:  # Predator logic
            if col in PREY:
                destroy_obj(col)
            if col in PREDATORS:
                # create_child(ship, col, PREDATORS)
                pass
        else:
            destroy_obj(col)
            destroy_obj(ship)

        update_map(anim)

    else:  # Proper move
        if debug == 1:
            print('Moving to', MAP[ship.x + xdirection][ship.y + ydirection])

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
        if MAP[ship.x][ship.y - 1] == s_empty:
            obj = Object(ship.x, ship.y - 1, s_missile, 0, -(ship.missile_speed))
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'down':
        if MAP[ship.x][ship.y + 1] == s_empty:
            obj = Object(ship.x, ship.y + 1, s_missile, 0, ship.missile_speed)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'right':
        if MAP[ship.x + 1][ship.y] == s_empty:
            obj = Object(ship.x + 1, ship.y, s_missile, ship.missile_speed, 0)
            MISSILES.append(obj)
        else:
            print("Can't shoot!")
    if ship.rotation == 'left':
        if MAP[ship.x - 1][ship.y] == s_empty:
            obj = Object(ship.x - 1, ship.y, s_missile, -(ship.missile_speed), 0)
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
                Object.object_count -= 1


def find_obj(x, y):
    """Returns the object"""
    for alist in FIELDS:
        for obj in alist:
            if x == obj.x and obj.y == y:
                return (obj)


def move_field(FIELD, arg1=0, arg2=0):
    """Moves all objects in the field"""
    if len(FIELD) != 0:
        COPY = FIELD.copy()  # [:]
        tuple(COPY)
        for obj in COPY:
            # if obj.xspeed != 0 and obj.yspeed !=0:
            if obj in FIELD:
                move_object(obj, arg1, arg2)


def random_walk(self):
    """Random walk"""
    self.xspeed = random.randrange(-1, 2)
    self.yspeed = random.randrange(-1, 2)


def select_and_follow(self, target_FIELD):
    """Randomly selects a target from a field and follows it untill it is dead"""

    # Create a memory system

    if len(target_FIELD) == 0:
        random_walk(self)
    else:
        target = find_closest(self, target_FIELD)
        # target = random.choice(target_FIELD)

        if target.x == self.x:
            self.xspeed = 0
        if target.y == self.y:
            self.yspeed = 0
        if target.x > self.x:
            self.xspeed = 1
        if target.x < self.x:
            self.xspeed = -1
        if target.y > self.y:
            self.yspeed = 1
        if target.y < self.y:
            self.yspeed = -1


def takeFirst(elem):
    return elem[0]


def find_closest(self, target_field):
    target_list = []
    for target in target_field:
        distance = abs(target.x - self.x) + abs(target.x - target.y)
        if distance == 1:
            return target
        target_list.append([distance, target])
    target_list = sorted(target_list, key=takeFirst)
    return target_list[0][1]


def update_stats(self):
    self.age += 1
    # if self.age > 76:
    #    destroy_obj(self)


def create_child(self, partner, field):
    # Fix spawning position
    birth = False
    if self.birth_rate > 0 and self.age > self.birth_age and partner.age > self.birth_age:
        xcord = self.x
        ycord = self.y
        try:
            if MAP[self.x - 1][self.y] == s_empty:
                birth = True
                xcord = self.x - 1
                ycord = self.y
            elif MAP[self.x + 1][self.y] == s_empty:
                birth = True
                xcord = self.x + 1
                ycord = self.y
            elif MAP[self.x][self.y - 1] == s_empty:
                birth = True
                xcord = self.x
                ycord = self.y - 1
            elif MAP[self.x][self.y + 1] == s_empty:
                birth = True
                xcord = self.x
                ycord = self.y + 1
        except:
            pass

        if birth == True:
            obj = Object(xcord, ycord, self.sprite)
            field.append(obj)
            self.birth_rate -= 1
            partner.birth_rate -= 1
            if self.birth_rate == 0:
                destroy_obj(self)
            #    print('Died at', self.x, self.y)
            if partner.birth_rate == 0:
                destroy_obj(partner)
            #    print('Partner died')
            # print("Child created! At", self.x, self.y)


def generate_obstacles(num):
    for i in range(num):
        randx = random.randrange(1, MAP_W)
        randy = random.randrange(1, MAP_H)
        if MAP[randx][randy] == s_empty:
            obs = Object(randx, randy, s_wall)
            WALLS.append(obs)


def generate_ai(num):
    for i in range(num):
        randx = random.randrange(1, MAP_W)
        randy = random.randrange(1, MAP_H)
        if MAP[randx][randy] == s_empty:
            obs = Object(randx, randy, s_ai)
            AIS.append(obs)


def generate_target(num):  # Useless
    for i in range(num):
        while True:
            randx = random.randrange(1, MAP_W - 1)
            randy = random.randrange(1, MAP_H - 1)
            randsx = random.randrange(-1, 2)
            randsy = random.randrange(-1, 2)
            if MAP[randx][randy] == s_empty:
                obs = Object(randx, randy, s_target, randsx, randsy)
                TARGETS.append(obs)
                break


def generate_objects(num, sprite, field):
    for i in range(num):
        while True:
            randx = random.randrange(1, MAP_W - 1)
            randy = random.randrange(1, MAP_H - 1)
            if MAP[randx][randy] == s_empty:
                obj = Object(randx, randy, sprite)
                field.append(obj)
                if field == PREDATORS or PREY:
                    obj.age = obj.birth_age
                break


def generate_border():
    for i in range(MAP_H):
        if MAP[0][i] == s_empty:
            obs = Object(0, i, s_wall)
            WALLS.append(obs)
    for i in range(MAP_H):
        if MAP[MAP_W - 1][i] == s_empty:
            obs = Object(MAP_W - 1, i, s_wall)
            WALLS.append(obs)
    for i in range(MAP_W):
        if MAP[i][MAP_H - 1] == s_empty:
            obs = Object(i, MAP_H - 1, s_wall)
            WALLS.append(obs)
    for i in range(MAP_W):
        if MAP[i][0] == s_empty:
            obs = Object(i, 0, s_wall)
            WALLS.append(obs)


# =============== MAIN LOOP =============== #
def main():

    simulation_tick = 0

    handling = False
    turn = True

    generate_border()  # Helps with out of index birth
    # generate_obstacles(300)
    generate_objects(50, s_small, PREY)
    generate_objects(6, s_predator, PREDATORS)

    OBJECTS.append(p_ship)
    # OBJECTS.append(e_ship)

    if len(OBJECTS) > 0:
        handling = True

    while True:
        update_map(1)
        turn = 2  # Input handling
        while turn != 0 and handling == True:
            for ship in OBJECTS:
                # 1 distance movement
                ship.xspeed = 0
                ship.yspeed = 0

                print('Make a move for', ship.sprite)
                inp = input('Input (w/s/a/d, f, h, i/k/j/l, b, x): ')

                # Move
                if inp == 'a':
                    ship.xspeed -= 1
                    turn -= 1
                    update_map(1)
                elif inp == 'd':
                    ship.xspeed += 1
                    turn -= 1
                    update_map(1)
                elif inp == 'w':
                    ship.yspeed -= 1
                    turn -= 1
                    update_map(1)
                elif inp == 's':
                    ship.yspeed += 1
                    turn -= 1
                    update_map(1)
                # Skip movement
                elif inp == 'h':
                    turn -= 1
                    handling = False
                # Exit
                elif inp == 'x':

                    sys.exit()
                # Break
                elif inp == 'b':
                    ship.yspeed = 0
                    ship.xspeed = 0
                    print('Breaking...')
                    turn = 0
                # Fire
                elif inp == 'f':
                    fire(ship)
                    turn = 0
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
                    turn = 0
                # No inputs afterwards
            move_field(OBJECTS, 1)

        move_field(MISSILES, 1)

        for obj in PREY:
            update_stats(obj)
            if MAP[obj.x + 1][obj.y] == s_empty \
                    or MAP[obj.x - 1][obj.y] == s_empty \
                    or MAP[obj.x][obj.y + 1] == s_empty \
                    or MAP[obj.x][obj.y - 1] == s_empty:
                random_walk(obj)
            else:
                obj.xspeed = 0
                obj.yspeed = 0

        move_field(PREY)

        for obj in PREDATORS:
            select_and_follow(obj, PREY)
            update_stats(obj)

        move_field(PREDATORS)

        if len(OBJECTS) == 0 and len(TARGETS) == 0 and len(AIS) == 0 and len(PREY) == 0 and len(PREDATORS):
           print('No more objects on the map')
           break
        print('Population:', Object.object_count)
        simulation_tick += 1
        print('Tick:', simulation_tick)

    print('program ended at the simulation tick', simulation_tick)
    input('Press to exit')

main()
