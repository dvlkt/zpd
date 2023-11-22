import os, sys, time
from pyboy import PyBoy,WindowEvent
import pygame
from random import *
config = {
    "gamerom_file": "T.gb",
    "game_wrapper": True,
    "window_scale": 3,
    "window_type": "headless"
}
pygame.init()
win=pygame.display.set_mode((600,600))
pyboy = PyBoy(**config)
tetris = pyboy.game_wrapper()
tetris.start_game()
config={
    "observation_type":"minimal",
    "action_type":"press"
    #"render_modes":["ansi"]
    }
OAG=pyboy.openai_gym(**config)#open_ai_gym
def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()
res=(160,144)
current_action=0
factions=[
    '(array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8))', #cleveland Z (Reverse Squigly)
    
    '(array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0], dtype=uint8))', #Rhode Island Z (Squiggly)
    
    '(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0], dtype=uint8))', #Teewee (T block)
    
    '(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0], dtype=uint8))', #Blue Ricky (reverse L)
    
    '(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0], dtype=uint8))', #Orange Ricky (L)

    '(array([0, 0, 0, 1, 1, 1, 1, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=uint8))', #Hero (long 4 tile boy)
    
    '(array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8), array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0], dtype=uint8))', #Smashboy (square)
    
    '(array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0], dtype=uint8), array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2], dtype=uint8))', #game over screen
    ]
names=[
    "Reverse Squiggly",
    "Squiggly",
    "T block",
    "L",
    "Reverse L",
    "Long 4 tile thing",
    "Square",
    "Lose",
    ]
key=""
lose_screen="['(array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],', '       [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],', '       [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],', '       [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],', '       [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],', '       [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],', '       [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],', '       [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],', '       [0, 0, 0, 1, 1, 1, 1, 1, 0, 0]], dtype=uint8), 0, False, {})']"
f2=[]
ttime=0
def detect_piece():
    try:
        if 1 in world[0][1]:
            return factions.index(str((world[0][1],world[0][2])))
        else:
            return None
    except:
        return None
def move(rot,pos):
    global sequence
    for i in range(rot):
        sequence.append(WindowEvent.PRESS_BUTTON_A)
        sequence.append(WindowEvent.RELEASE_BUTTON_A) #rotates rot times
    for i in range(abs(5-pos)):
        if pos>5:
            sequence.append(WindowEvent.PRESS_ARROW_RIGHT)
            sequence.append(WindowEvent.RELEASE_ARROW_RIGHT)
        else:
            sequence.append(WindowEvent.PRESS_ARROW_LEFT)
            sequence.append(WindowEvent.RELEASE_ARROW_LEFT)
    for i in range(4):
        sequence.append(WindowEvent.PRESS_ARROW_DOWN)
        sequence.append(WindowEvent.RELEASE_ARROW_DOWN)
run=True
last_piece=-1
sequence=[]
psight=""
extra_timer=0
clock=pygame.time.Clock()
moves_in=0
score=0
psightmax=-9
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    ttime+=1
    pyboy.tick()
    world=OAG.step(current_action)
    pkey=key
    game_lost=False
    for i in world[0]:
        if 2 in i:
            game_lost=True
    #if world[1]!=0:
    #    print(world[1],world[2],world[3])
    if not game_lost:
        if len(sequence)==0:
            is_piece=detect_piece()
            if is_piece!=None:
                sight=[0 for i in range(10)]
                for i1 in range(17):
                    #print("'"+str(world[0][i1])+"'")
                    if str(world[0][17-i1])=='[0 0 0 0 0 0 0 0 0 0]':
                        break
                i1+=1
                for i in range(i1):
                    for i2 in range(10):
                        if world[0][17-i][i2]==1:
                            sight[i2]=i+1
                sightmax=max(sight)
                sightmin=min(sight)
                if sightmax<psightmax:
                    #print(p_world)
                    #print(world)
                    pygame.image.save(win,"tetris.png")
                while sightmax<psightmax:
                    score+=abs(sightmax-psightmax)*100
                    psightmax-=1
                    print(score)
                sight=[i-sightmin for i in sight]
                sight=str(sight)
                psightmax=sightmax
                rt=randint(0,3) #random rotation
                ps=randint(0,9) #random position
                """
                Here does the amazing stuff
                """
                move(rt,ps)
                moves_in+=1
                clock.tick(1)
        else:
            if sequence[-1]!=-2:
                pyboy.send_input(sequence[0])
            sequence.pop(0)
    else:
        if moves_in!=0:
            print("Game Lost in",moves_in,"Moves")
        moves_in=0
        psight=""
        psightmax=-9
        sequence.append(WindowEvent.PRESS_BUTTON_A)
        sequence.append(WindowEvent.RELEASE_BUTTON_A)
    pil_image = pyboy.screen_image()
    p_world=world
    win.blit(pygame.transform.scale(pilImageToSurface(pyboy.screen_image()),win.get_size()),(0,0))
    #pil_image.save('screenshot.png')
    pygame.display.update()
pyboy.stop()
