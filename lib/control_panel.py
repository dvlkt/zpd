import pygame, pygame.gfxdraw
import data, algorithm

WINDOW_WIDTH = 0 # TODO
WINDOW_HEIGHT = 0 # TODO
VIEW_COLORS = [(30, 27, 20), (237, 49, 49), (49, 71, 237), (80, 242, 21), (242, 55, 236), (242, 123, 19), (237, 106, 198)]

pygame.init()


# Utility function to handle text rendering easily
fonts = {}
texts = {}
def _render_text(value, pos, size, color=(0, 0, 0), serif=False):
	if serif:
		font_path = "resources/dm-serif-text-regular.ttf"
	else:
		font_path = "resources/inter-regular.ttf"

	if fonts.get(size) == None:
		fonts[size] = pygame.font.Font(font_path, size)
	
	if texts.get(value) == None:
		texts[value] = fonts[size].render(value, True, color)
	
	window.blit(texts[value], pos)


def _render_button(label, pos, on_click):
	pygame.draw.rect(window, (193, 175, 131), (pos[0], pos[1], 200, 25), border_radius=10)
	_render_text(label, (pos[0] + 2, pos[1] + 2), 17)

	if pygame.mouse.get_pressed()[0]:
		mpos = pygame.mouse.get_pos()
		if mpos[0] > pos[0] and mpos[1] > pos[1] and mpos[0] < pos[0] + 200 and mpos[1] < pos[1] + 25:
			on_click()


window = None
def init():
	global window
	window = pygame.display.set_mode((700, 500))
	pygame.display.set_caption("Kontroles panelis")


is_algorithm_selection_open = False
algorithm_selection = pygame.Surface((700, 500))
def process():
	global is_algorithm_selection_open, algorithm_selection

	for event in pygame.event.get():
		pass

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
		if not is_algorithm_selection_open:
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

	# Copyright notice
	_render_text("© 2023, Dāvis Lektauers un Kazimirs Kārlis Brakovskis", (5, 480), 12)

	# Algorithm selection
	def select_algorithm(i):
		global is_algorithm_selection_open
		algorithm.set_algorithm(algorithm.available[i])
		is_algorithm_selection_open = False
	if is_algorithm_selection_open:
		pygame.draw.rect(window, (30, 27, 20), (0, 0, 700, 500))
		for i in range(len(algorithm.available)):
			_render_button(algorithm.available[i], (250, 10 + i * 35), lambda: select_algorithm(i))
	
	pygame.display.update()
	pygame.event.pump()