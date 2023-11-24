from math import pi, sin, cos, atan2
from random import random, uniform
import json

import pygame
import requests

session = requests.Session()

print("Mašīnmācīšanās programmai izmantojiet portu 1782!\n")

class Pong:
    def __init__(self):
        self.score = 0

        self.ball = {
            "x_pos": 0,
            "y_pos": 0,
            "x_speed": 0,
            "y_speed": 0,
        }
        self.ball_speed = 1/5 # how many screens can it travel each frame
        self.relative_ball_size = 0.05 # size of the ball relative to the screen size
        self.random_ball_direction(random())
        
        self.pad_position = [0, 0] # position of the two pads relative to the center of the screen (-1 is bottom, 1 is top, 0 is perfectly center)
        self.pad_speed = 1/10
        self.relative_pad_size = 0.2 # size of the ball relative to the screen size

    def random_ball_direction(self, direction=0):
        if direction < 0.5: # Left
            angle = uniform(2.356, 3.927) # 135deg to 225deg
        else: # Right
            angle = uniform(-0.785, 0.785) # -45deg to 45deg

        self.ball["x_speed"] = cos(angle) * self.ball_speed
        self.ball["y_speed"] = sin(angle) * self.ball_speed
    
    def straight_ball_direction(self, direction=0):
        if direction < 0.5:
            self.ball["x_speed"] = -self.ball_speed
        else:
            self.ball["x_speed"] = self.ball_speed
        
        self.ball["y_speed"] = 0
    
    def opposite_ball_direction(self):
        self.ball["x_speed"] = -self.ball["x_speed"]
        self.ball["y_speed"] = -self.ball["y_speed"]

    def next_frame(self):
        self.score += 1

        self.ball["x_pos"] += self.ball["x_speed"]
        self.ball["y_pos"] += self.ball["y_speed"]

        ## Top/bottom collision ##
        if self.ball["y_pos"] < -1 + self.relative_ball_size:
            self.ball["y_pos"] = -2 + self.relative_ball_size * 2 - self.ball["y_pos"]
            self.ball["y_speed"] *= -1
        
        if self.ball["y_pos"] > 1 - self.relative_ball_size:
            self.ball["y_pos"] = 2 - self.relative_ball_size * 2 - self.ball["y_pos"]
            self.ball["y_speed"] *= -1
        
        ## Pad collision ##
        if self.ball["x_pos"] < -0.9 + self.relative_ball_size and abs(self.ball["y_pos"] - self.pad_position[0]) < self.relative_pad_size:
            self.opposite_ball_direction()
        
        if self.ball["x_pos"] > 0.9 - self.relative_ball_size and abs(self.ball["y_pos"] - self.pad_position[1]) < self.relative_pad_size:
            self.opposite_ball_direction()

        ## Wall collision ##
        is_lost = False
        if (self.ball["x_pos"] < -1.15 + self.relative_ball_size) or \
            (self.ball["x_pos"] > 1.15 - self.relative_ball_size):

            is_lost = True
        
        ## Send server request ##
        if self.ball["x_speed"] > 0:
            state = (abs(round(1 - self.ball["x_pos"], 1)), abs(round(self.ball["y_pos"] - self.pad_position[1], 1)))
        else:
            state = (abs(round(1 + self.ball["x_pos"], 1)), abs(round(self.ball["y_pos"] - self.pad_position[0], 1)))
        print(state)
        req = session.post("http://localhost:1782", json={
            "state": json.dumps(state),
            "score": self.score,
            "lost": is_lost
        })

        if req.json().get("action") == None: return
        action = req.json()["action"]
        if self.ball["x_speed"] < 0:
            if action == 0 and self.pad_position[0] < 1:  # Left pad up
                self.pad_position[0] += self.pad_speed
            elif action == 1 and self.pad_position[0] > -1: # Left pad down
                self.pad_position[0] -= self.pad_speed
        else:
            if action == 0 and self.pad_position[1] < 1: # Right pad up
                self.pad_position[1] += self.pad_speed
            elif action == 1 and self.pad_position[1] > -1: # Right pad down
                self.pad_position[1] -= self.pad_speed
        
        if req.json().get("reset") == None: return
        if req.json()["reset"]:
            self.score = 0
            self.ball["x_pos"] = 0
            self.ball["y_pos"] = 0
            self.random_ball_direction(random())
            self.pad_position = [0, 0]

        ## Game lost ##
        if is_lost:
            self.score = 0
            self.ball["x_pos"] = 0
            self.ball["y_pos"] = 0
            self.random_ball_direction(random())
        
    def first_frame(self):
        pygame.init()
        self.screen_size = [pygame.display.get_desktop_sizes()[0][1] / 10 * 8.5 for i in range(2)]
        self.screen = pygame.display.set_mode((self.screen_size))
        self.s = pygame.Surface((500, 500))
        
        ## Initial server request ##
        session.post("http://localhost:1782", json={
            "actionCount": 2,
            "state": "[0, 0]",
            "score": self.score,
            "lost": False
        })

    def draw_frame(self):
        self.s.fill((0, 0, 0))
        
        # Ball
        pygame.draw.rect(self.s, (255, 255, 255),
            (250 + (self.ball["x_pos"] - self.relative_ball_size) * 250,
            250 + (self.ball["y_pos"] - self.relative_ball_size) * 250,
            self.relative_ball_size * 500,
            self.relative_ball_size * 500))
        
        # Pads
        pygame.draw.rect(self.s, (255, 255, 255), (0, 250 + self.pad_position[0] * 250 - self.relative_pad_size * 125, 10, self.relative_pad_size * 500))
        pygame.draw.rect(self.s, (255, 255, 255), (490, 250 + self.pad_position[1] * 250 - self.relative_pad_size * 125, 10, self.relative_pad_size * 500))

        self.screen.blit(pygame.transform.scale(self.s, self.screen_size), (0, 0))
        pygame.display.update()
        pygame.event.get()

clock = pygame.time.Clock()
p = Pong()
p.first_frame()
while True:
    clock.tick(10)
    p.next_frame()
    p.draw_frame()
