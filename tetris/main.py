import os, sys, time
from pyboy import PyBoy, WindowEvent
import pygame
import requests
from random import *

session = requests.Session()

pyboy_config = {
    "gamerom_file": os.path.join(os.path.dirname(os.path.realpath(__file__)), "tetris.gb"),
    "game_wrapper": True,
    "window_scale": 3,
    "window_type": "headless",
}
pygame.init()
win = pygame.display.set_mode((600,600))
pyboy = PyBoy(**pyboy_config)

tetris = pyboy.game_wrapper()
tetris.start_game()
oag_config = {
    "observation_type": "minimal",
    "action_type": "press",
    #"render_modes": ["ansi"],
}
oag = pyboy.openai_gym(**oag_config)

def pil_image_to_surface(pil_image):
    return pygame.image.fromstring(
        pil_image.tobytes(), pil_image.size, pil_image.mode).convert()

res = (160, 144)
factions = [
    "(array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8))", # cleveland Z (Reverse Squigly)
    "(array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0], dtype=uint8))", # Rhode Island Z (Squiggly)
    "(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0], dtype=uint8))", # Teewee (T block)
    "(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0], dtype=uint8))", # Blue Ricky (reverse L)
    "(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0], dtype=uint8))", # Orange Ricky (L)
    "(array([0, 0, 0, 1, 1, 1, 1, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=uint8))", # Hero (long 4 tile boy)
    "(array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8))", # Smashboy (square)    
    "(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2], dtype=uint8))", # game over screen
]
names = [
    "Reverse Squiggly",
    "Squiggly",
    "T block",
    "L",
    "Reverse L",
    "Long 4 tile thing",
    "Square",
    "Lose",
]
lose_screen = "['(array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],', '       [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],', '       [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],', '       [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],', '       [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],', '       [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],', '       [0, 0, 0, 1, 1, 1, 1, 1, 0, 0]], dtype=uint8), 0, False, {})']"

def detect_piece():
    try:
        if 1 in world[0][1]:
            return factions.index(str((world[0][1], world[0][2])))
        else:
            return None
    except:
        return None

def move(rot, pos):
    global sequence
    for i in range(rot):
        sequence.append(WindowEvent.PRESS_BUTTON_A)
        sequence.append(WindowEvent.RELEASE_BUTTON_A) # rotates rot times
    for i in range(abs(5-pos)):
        if pos > 5:
            sequence.append(WindowEvent.PRESS_ARROW_RIGHT)
            sequence.append(WindowEvent.RELEASE_ARROW_RIGHT)
        else:
            sequence.append(WindowEvent.PRESS_ARROW_LEFT)
            sequence.append(WindowEvent.RELEASE_ARROW_LEFT)
    for i in range(4):
        sequence.append(WindowEvent.PRESS_ARROW_DOWN)
        sequence.append(WindowEvent.RELEASE_ARROW_DOWN)

run = True
time = 0
clock = pygame.time.Clock()
last_piece = -1
sequence = []
psight = ""
extra_timer = 0
moves_in = 0
score = 0
prev_sight_max = -9

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    time += 1
    pyboy.tick()
    world = oag.step(0)
    game_lost = False

    for i in world[0]:
        if 2 in i:
            game_lost = True

    if not game_lost:
        if len(sequence) == 0:
            is_piece = detect_piece()
            if is_piece != None:
                sight = [0 for i in range(10)]
                for i1 in range(17):
                    if str(world[0][17 - i1]) == "[0 0 0 0 0 0 0 0 0 0]":
                        break
                i1 += 1
                for i in range(i1):
                    for i2 in range(10):
                        if world[0][17-i][i2] == 1:
                            sight[i2] = i+1
                
                sight_max = max(sight)
                sight_min = min(sight)
                
                while sight_max < prev_sight_max:
                    score += abs(sight_max - prev_sight_max) * 100
                    prev_sight_max -= 1
                
                sight = [i - sight_min for i in sight]
                sight = str(sight)
                prev_sight_max = sight_max
                rt = randint(0,3) #random rotation
                ps = randint(0,9) #random position

                move(rt, ps)
                moves_in += 1
                clock.tick(100)
        else:
            if sequence[-1] != -2:
                pyboy.send_input(sequence[0])
            sequence.pop(0)
    else:
        if moves_in != 0:
            print("Spēle zaudēta", moves_in, "gājienos")
        
        moves_in = 0
        psight = ""
        prev_sight_max = -9

        sequence.append(WindowEvent.PRESS_BUTTON_A)
        sequence.append(WindowEvent.RELEASE_BUTTON_A)
    
    prev_world = world

    pil_image = pyboy.screen_image()
    win.blit(pygame.transform.scale(pil_image_to_surface(pyboy.screen_image()), win.get_size()), (0, 0))
    pygame.display.update()

pyboy.stop()