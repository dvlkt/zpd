import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide" # Hide the pygame welcome message
import pygame, pygame.gfxdraw
import data, algorithm

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
VIEW_COLORS = [(30, 27, 20), (237, 49, 49), (49, 71, 237), (80, 242, 21), (242, 55, 236), (242, 123, 19), (237, 106, 198)]

pygame.init()


# Utility function to handle text rendering easily
fonts = {}
texts = {}
def _render_text(value, pos, size, color=(0, 0, 0), serif=False):
    if serif:
        font_path = os.path.join(data.directory, "resources/dm-serif-text-regular.ttf")
    else:
        font_path = os.path.join(data.directory, "resources/inter-regular.ttf")

    if fonts.get(size) == None:
        fonts[size] = pygame.font.Font(font_path, size)
    
    text_id = f"{value} {size} {color} {serif}"

    if texts.get(text_id) == None:
        texts[text_id] = fonts[size].render(value, True, color)
    
    window.blit(texts[text_id], pos)


def _render_button(label, pos, on_click):
    pygame.draw.rect(window, (193, 175, 131), (pos[0], pos[1], 200, 25), border_radius=10)
    _render_text(label, (pos[0] + 4, pos[1] + 2), 17)

    if pygame.mouse.get_pressed()[0]:
        mpos = pygame.mouse.get_pos()
        if mpos[0] > pos[0] and mpos[1] > pos[1] and mpos[0] < pos[0] + 200 and mpos[1] < pos[1] + 25:
            on_click()


_pressed_keys = []
_input_values = {}
def _render_input(name, pos):
    if _input_values.get(name) == None:
        _input_values[name] = ""
    
    for i in _pressed_keys:
        if i == "[BACKSPACE]" and len(_input_values[name]) > 0:
            _input_values[name] = _input_values[name][:-1]
        else:
            _input_values[name] += i

    pygame.draw.rect(window, (193, 175, 131), (pos[0], pos[1], 400, 25), border_radius=10)
    _render_text(f"{_input_values[name]}|", (pos[0] + 4, pos[1] + 2), 17)

def _get_input_value(name):
    if _input_values.get(name) == None:
        _input_values[name] = ""
    
    return _input_values[name]

def _set_input_value(name, value):
    if _input_values.get(name) == None:
        _input_values[name] = ""
    
    _input_values[name] = value


window = None
def init():
    global window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Kontroles panelis")


is_algorithm_selection_open = False
algorithm_selection = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
is_save_menu_open = False
is_load_menu_open = False
def process():
    global _pressed_keys, is_algorithm_selection_open, algorithm_selection, is_save_menu_open, is_load_menu_open

    _pressed_keys = []
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 8:
                _pressed_keys.append("[BACKSPACE]")
            else:
                _pressed_keys.append(event.unicode)

    window.fill((239, 227, 198))

    # Title
    game_title = data.game_title
    if game_title == None:
        game_title = "Nekas netiek spēlēts..."
    _render_text(f"{game_title}", (10, 0), 35, color=(30, 27, 20), serif=True)

    # Algorithm indicator
    algorithm_name = algorithm.current_name
    _render_text(f"Izmantotais algoritms: {algorithm_name}", (10, 45), 18)

    # Change algorithm
    def open_algorithm_selection():
        global is_algorithm_selection_open
        is_algorithm_selection_open = True
    _render_button(f"Mainīt algoritmu", (10, 70), open_algorithm_selection)

    # Simplified view
    _render_text("Vienkāršots skats:", (10, 110), 18)
    if data.game_view_dimensions != None and data.game_view != None:
        view_pixel_size = max(100 / data.game_view_dimensions[0], 100 / data.game_view_dimensions[1])
        for x in range(len(data.game_view)):
            for y in range(len(data.game_view[x])):
                pygame.draw.rect(window, VIEW_COLORS[data.game_view[x][y]], (10 + x * view_pixel_size, 135 + y * view_pixel_size, view_pixel_size, view_pixel_size))
    _render_text(f"Rezultāts: {data.game_score}", (10, 235), 12)

    # Saving and loading buttons
    def open_save_menu():
        global is_save_menu_open
        is_save_menu_open = True
    _render_button(f"Saglabāt stāvokli", (10, 265), open_save_menu)

    def open_load_menu():
        global is_load_menu_open
        is_load_menu_open = True
    _render_button(f"Ielādēt stāvokli", (220, 265), open_load_menu)

    # Copyright notice
    _render_text("© 2023, Dāvis Lektauers un Kazimirs Kārlis Brakovskis", (5, WINDOW_HEIGHT - 20), 12)

    # Algorithm selection
    def select_algorithm(i):
        global is_algorithm_selection_open
        algorithm.set_algorithm(algorithm.available[i])
        is_algorithm_selection_open = False
    
    if is_algorithm_selection_open:
        pygame.draw.rect(window, (30, 27, 20), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        for i in range(len(algorithm.available)):
            _render_button(algorithm.available[i], (250, 10 + i * 35), lambda: select_algorithm(i))
    
    # Save/load menu
    def save_file():
        global is_save_menu_open
        is_save_menu_open = False
        _set_input_value("file_name", "")
    
    def load_file():
        global is_load_menu_open
        is_load_menu_open = False
        _set_input_value("file_name", "")
    
    def cancel_file():
        global is_save_menu_open, is_load_menu_open
        is_save_menu_open = False
        is_load_menu_open = False
        _set_input_value("file_name", "")
    
    if is_save_menu_open or is_load_menu_open:
        if is_save_menu_open:
            input_menu_title = "Saglabāt stāvokli"
            accept_btn_label = "Saglabāt"
        else:
            input_menu_title = "Ielādēt stāvokli"
            accept_btn_label = "Ielādēt"
        
        pygame.draw.rect(window, (30, 27, 20), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        _render_text(input_menu_title, (10, 10), 32, color=(255, 255, 255), serif=True)
        _render_text("Ievadiet faila nosaukumu:", (10, 60), 18, color=(255, 255, 255))
        _render_input("file_name", (10, 90))

        if is_save_menu_open:
            _render_button("Saglabāt", (10, 125), save_file)
        else:
            _render_button("Ielādēt", (10, 125), load_file)
        
        _render_button("Atcelt", (10, 160), cancel_file)
    
    pygame.display.update()
    pygame.event.pump()