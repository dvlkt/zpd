import os

game_title = None
def set_game_title(value):
    global game_title
    game_title = value

game_score = 0
def set_game_score(value):
    global game_score
    game_score = value

game_state = []
def set_game_state(value):
    global game_state
    game_state = value

game_state_size = None
def set_game_state_size(value):
    global game_state_size
    game_state_size = value

game_action_count = None
def set_game_action_count(value):
    global game_action_count
    game_action_count = value

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)))