#!/usr/bin/python3

# ========================= LIBRARIES ========================= #
import pygame
import sys
import serial
import re
import requests


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


server_ip = 'http://10.0.1.30:8080'

class data:
    window_size = 800
    size = 100

# ============= Usage ============= #

try:
    port = sys.argv[1]
    baud = int(sys.argv[2])
    data.window_size = int(sys.argv[3])
    data.size = int(sys.argv[4])
except:
    print(f'Usage ./RoboPlace.py <port> <baud> <window size> <size>')
    #print(f'Or ./snak.py --noserial')
    print(f'Example: ./RoboPlace.py /dev/ttyACM0 115200 800 100')
    exit()


# ========================= Logger class ========================= #


class logger:
    file_num = 0
    file = open(f'logs/log{file_num}.txt', 'a')
    
    def check_size():
        if logger.file.tell() > 32767:
            print(f'Closing file {logger.file_num}')
            logger.file.close()
            file_num = file_num+1
            logger.file = open(f'logs/log{logger.file_num}.txt', "a")

    def log(data):
        logger.file.write(f'{data}\n')

    def close_file():
        logger.file.close()


# ========================= GAME class ========================= #


class Game:
    id_timeouts = {}

    timeout_interval = 10000 # 10s
    
    size = data.size
    window_size = data.window_size

    changes = []

    def handle_cmds(toks):
        #   toks[0]  toks[1] toks[2] toks[3] toks[4]
        #    80001    paint    10      10      red
        user_id = toks[0]
        cmd = toks[1]
        
         # Handle timeouts
        if user_id in Game.id_timeouts:
            return
        else:
            Game.id_timeouts[user_id] = pygame.time.get_ticks()
        try:
            if cmd == 'paint':
                if toks[4] not in list(Screen.COLOR.keys()):
                    print(f'{user_id} >>> {toks[1]} {toks[2]} {toks[3]} {toks[4]} (WRONG COLOR)')
                else:
                    print(f'{user_id} >>> {toks[1]} {toks[2]} {toks[3]} {toks[4]}')
                    Game.changes.append([toks[2], toks[3], toks[4]])
                    logger.log(f'{user_id} {toks[1]} {toks[2]} {toks[3]} {toks[4]}')

                    obj = {toks[2] + "_" + toks[3]: toks[4]}
                    print(obj)
                    req = requests.post(url=server_ip +'/post', data=obj)

            elif cmd == 'test':
                print(f'{user_id} >>> {toks[1]}')
        except Exception:
            return


# ========================= SCREEN class ========================= #

class Screen:
    colors = [

        "white",
        "platinum",
        "grey",
        "black",
        "pink",
        "red",
        "orange",
        "brown",
        "yellow",
        "lime",
        "green",
        "cyan",
        "lblue",
        "blue",
        "mauve",
        "purple" 
    
    ]
    # color list
    COLOR = {
        "white":    pygame.Color("#FFFFFF"),
        "platinum": pygame.Color("#E4E4E4"),
        "grey":     pygame.Color("#888888"),
        "black":    pygame.Color("#222222"),
        "pink":     pygame.Color("#FFA7D1"),
        "red":      pygame.Color("#E50000"),
        "orange":   pygame.Color("#E59500"),
        "brown":    pygame.Color("#A06A42"),
        "yellow":   pygame.Color("#E5D900"),
        "lime":     pygame.Color("#94E044"),
        "green":    pygame.Color("#02BE01"),
        "cyan":     pygame.Color("#00D3DD"),
        "lblue":    pygame.Color("#0083C7"),
        "blue":     pygame.Color("#0000EA"),
        "mauve":    pygame.Color("#CF6EE4"),
        "purple":   pygame.Color("#820080")
    }

    DEFAULT_COLOR = "white"
    

    pixels = []
    pixel_size = Game.window_size / Game.size

    # create array of Game size
    def init():
        Screen.pixels = [['white' for i in range(Game.size)] for j in range(Game.size)]
    
    # draw changes to list
    def draw_changes():
        for change in Game.changes:
            x = int(change[0])
            y = int(change[1])
            color = str(change[2])
            Screen.pixels[x][y] = color
            obj = "{"+str(x) + "_" + str(y) + ":"+ str(Screen.colors.index(color)) + "}"
            x = requests.post('http://10.0.1.30:8080/post', json = obj)
            
            #print(f'change {change}')

        # resets the changes
        Game.changes = []

    # draw pixel list to screen
    def update(surface):
        for y in range(Game.size):
            for x in range(Game.size):
                pygame.draw.rect(surface, Screen.COLOR[Screen.pixels[x][y]], (x*Screen.pixel_size, y*Screen.pixel_size, Screen.pixel_size, Screen.pixel_size))
    
        
# ========================= Functions ========================= #

# parser
def parse(input):
    try:
        input = input.decode('ascii').rstrip().lstrip()
    except Exception:
        return None
    data = re.split(r" +", input)

    if len(data) < 2:
        return None

    return data


# ========================= Main Loop ========================= #


def main():

    # Initialize pygame
    screen = pygame.display.set_mode([Game.window_size, Game.window_size])
    pygame.init()

    pygame.display.set_caption('RoboPlace')
    pygame.font.init()


    Screen.init()
    Screen.update(screen)
    pygame.display.flip()

    
    # Variable to keep the main loop running
    running = True

    pygame.time.set_timer(pygame.USEREVENT, 5000) # every 5s
    pygame.time.set_timer(pygame.USEREVENT_DROPFILE, 100) # every 100 ms

    # serial setup
    with serial.Serial(port, baud, timeout=0) as ser:
        while running:
            event = pygame.event.wait()
            if True:
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                
                # Did the user click the window close button? If so, stop the loop.
                elif event.type == QUIT:
                    running = False

                # Every 100 ms
                elif event.type == pygame.USEREVENT_DROPFILE:
                    # checl if log file is too large
                    logger.check_size()
                    while True:
                        # read serial
                        line = ser.readline()
                        if len(line) == 0:
                            break  # break from loop
                        toks = parse(line)
                        if toks is None:
                            continue  # next loop
                        Game.handle_cmds(toks)
                        
                
                # Every 5s
                elif event.type == pygame.USEREVENT:
                    Screen.draw_changes()
                    Screen.update(screen)

                    pygame.display.flip()
                    ticks = pygame.time.get_ticks()

                    for id in list(Game.id_timeouts.keys()):
                        if Game.id_timeouts[id] < ticks - Game.timeout_interval:
                            Game.id_timeouts.pop(id)
                            #print(f'ID {id} is removed from timeouts')

        # close log file
        logger.close_file()

        # close Game
        pygame.quit()
        exit()



# call main function
main()
