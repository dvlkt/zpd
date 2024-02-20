import os, random
import pygame
import requests

CWD = os.path.join(os.path.dirname(os.path.realpath(__file__)))
SURFACE_SIZE = (224, 248)
UPSCALE = 3
SHOW_WINDOW = False
PORT = 1785

session = requests.Session()

class Ghost:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Game:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.score = 0
        self.pos = [13, 23]
        self.dir = -1
        self.ghosts = [Ghost(12, 14), Ghost(14, 14), Ghost(16, 14), Ghost(14, 11)]

        # Parse the layout
        self.layout = [] # 0 = wall, 1 = empty space, 2 = orb, 3 = big orb
        layout_img = pygame.image.load(os.path.join(CWD, "resources/layout.png"))
        for x in range(layout_img.get_width()):
            col = []
            for y in range(layout_img.get_height()):
                val = layout_img.get_at([x, y])
                if val == (33, 33, 255, 255):
                    col.append(0)
                elif val == (102, 102, 102, 255):
                    col.append(1)
                elif val == (51, 51, 51, 255):
                    col.append(3)
                else:
                    col.append(2)
            self.layout.append(col)
    
    def is_pos_empty(self, x: int, y: int):
        if x < 0 or x >= len(self.layout) or y < 0 or y >= len(self.layout[x]):
            return True
        if self.layout[x][y] == 0:
            return False
        for g in self.ghosts:
            if g.x == x and g.y == y:
                return False
        return True
    
    def get_pos(self, x: int, y: int):
        if x < 0 or x >= len(self.layout) or y < 0 or y >= len(self.layout[x]):
            return 1
        return self.layout[x][y]
    
    def get_state(self):
        tl = self.get_pos(self.pos[0]-1, self.pos[1]-1)
        t = self.get_pos(self.pos[0], self.pos[1]-1)
        tr = self.get_pos(self.pos[0]+1, self.pos[1]-1)
        l = self.get_pos(self.pos[0]-1, self.pos[1])
        r = self.get_pos(self.pos[0]+1, self.pos[1])
        bl = self.get_pos(self.pos[0]-1, self.pos[1]+1)
        b = self.get_pos(self.pos[0], self.pos[1]+1)
        br = self.get_pos(self.pos[0]+1, self.pos[1]+1)
        return f"{tl}{t}{tr}{l}{r}{bl}{b}{br}"

    def next_frame(self):
        # Ghost movement
        for g in self.ghosts:
            possible_directions = []
            if self.is_pos_empty(g.x-1, g.y):
                possible_directions.append("left")
            if self.is_pos_empty(g.x, g.y-1):
                possible_directions.append("up")
            if self.is_pos_empty(g.x+1, g.y):
                possible_directions.append("right")
            if self.is_pos_empty(g.x, g.y+1):
                possible_directions.append("down")
            
            if len(possible_directions) == 0:
                continue
            direction = random.choice(possible_directions)
            if direction == "left":
                g.x -= 1
            elif direction == "up":
                g.y -= 1
            elif direction == "right":
                g.x += 1
            elif direction == "down":
                g.y += 1
            
            # Looping around
            if g.x < 0:
                g.x = len(self.layout) - 2
            if g.x > len(self.layout) - 2:
                g.x = 0
        
        # Orb eating
        if self.layout[self.pos[0]][self.pos[1]] == 2:
            self.score += 1
            self.layout[self.pos[0]][self.pos[1]] = 1
        elif self.layout[self.pos[0]][self.pos[1]] == 3:
            self.score += 5
            self.layout[self.pos[0]][self.pos[1]] = 1
        
        # Pacman movement
        if self.dir == 0:
            if self.is_pos_empty(self.pos[0]-1, self.pos[1]):
                self.pos[0] -= 1
            if not self.is_pos_empty(self.pos[0]-1, self.pos[1]) or \
            self.is_pos_empty(self.pos[0], self.pos[1]-1) or self.is_pos_empty(self.pos[0], self.pos[1]+1):
                self.dir = -1
        
        if self.dir == 1:
            if self.is_pos_empty(self.pos[0], self.pos[1]-1):
                self.pos[1] -= 1
            if not self.is_pos_empty(self.pos[0], self.pos[1]-1) or \
            self.is_pos_empty(self.pos[0]-1, self.pos[1]) or self.is_pos_empty(self.pos[0]+1, self.pos[1]):
                self.dir = -1
        
        if self.dir == 2:
            if self.is_pos_empty(self.pos[0]+1, self.pos[1]):
                self.pos[0] += 1
            if not self.is_pos_empty(self.pos[0]+1, self.pos[1]) or \
            self.is_pos_empty(self.pos[0], self.pos[1]-1) or self.is_pos_empty(self.pos[0], self.pos[1]+1):
                self.dir = -1
        
        if self.dir == 3:
            if self.is_pos_empty(self.pos[0], self.pos[1]+1):
                self.pos[1] += 1
            if not self.is_pos_empty(self.pos[0], self.pos[1]+1) or \
            self.is_pos_empty(self.pos[0]-1, self.pos[1]) or self.is_pos_empty(self.pos[0]+1, self.pos[1]):
                self.dir = -1
        
        # Looping around
        if self.pos[0] < 0:
            self.pos[0] = len(self.layout) - 2
        if self.pos[0] > len(self.layout) - 2:
            self.pos[0] = 0
        
        # Death
        has_lost = False
        for g in self.ghosts:
            if g.x == self.pos[0] and g.y == self.pos[1]:
                has_lost = True
                break
        
        # Send server request
        if self.dir == -1 or has_lost:
            req = session.post(f"http://localhost:{PORT}", json={
                "state": self.get_state(),
                "score": self.score,
                "lost": has_lost
            })
            self.dir = req.json()["action"]

            if req.json()["reset"] or has_lost:
                self.reset()
                return
        
    def first_frame(self):
        pygame.init()
        self.win = pygame.display.set_mode((SURFACE_SIZE[0] * UPSCALE, SURFACE_SIZE[1] * UPSCALE))
        pygame.display.set_caption("Pac-Man")
        self.s = pygame.Surface(SURFACE_SIZE)

        print(f"Mašīnmācīšanās programmai izmantojiet portu {1785}!\n")

        # Initial server request
        session.post(f"http://localhost:{PORT}", json={
            "actionCount": 4,
            "state": self.get_state(),
            "score": self.score,
            "lost": False
        })

    def draw_frame(self):
        self.s.fill((0, 0, 0))

        # Background
        self.s.blit(pygame.image.load(os.path.join(CWD, "resources/background.png")), (0, 0))

        # Orbs
        for x in range(len(self.layout)):
            for y in range(len(self.layout[x])):
                if self.layout[x][y] == 2:
                    self.s.blit(pygame.image.load(os.path.join(CWD, "resources/orb.png")), (x*8, y*8))
                if self.layout[x][y] == 3:
                    self.s.blit(pygame.image.load(os.path.join(CWD, "resources/big_orb.png")), (x*8, y*8))
        
        # Ghosts
        for g in self.ghosts:
            self.s.blit(pygame.image.load(os.path.join(CWD, "resources/ghost.png")), (g.x*8-7, g.y*8-3))
        
        # Agent
        self.s.blit(pygame.image.load(os.path.join(CWD, "resources/agent.png")), (self.pos[0]*8-2, self.pos[1]*8-3))
            
        self.win.blit(pygame.transform.scale(self.s, self.win.get_size()), (0, 0))
        pygame.display.update()
        pygame.event.get()

game = Game()
game.first_frame()
while True:
    game.next_frame()
    if SHOW_WINDOW:
        game.draw_frame()
