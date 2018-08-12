#imported modules
import curses
import random
import time

#curses setup
screen = curses.initscr()
screen.keypad(True)
screen.timeout(25)
curses.noecho()
curses.curs_set(False)

#misc variables
map_y = 30
map_x = 100
screen_y, screen_x = screen.getmaxyx()
camera_max_y = map_y - screen_y
camera_max_x = map_x - screen_x
camera_y = 0
camera_x = 0
player_y = 4
player_x = 4

#main arrays
game_map = []
game_screen = []
ui_screen = []

#game object icons
filler = " "
player_icon = "@"
door_icon = "▒"
wall_icon = "█"

#make the array game_map and fill it with filler arrays
def make_map():
	for a in range(map_y):
		game_map.append([])
	for a in range(map_y):
		for b in range(map_x):
			game_map[a].append([["filler", filler]])

#make the array game_screen and fill it with filler
def make_screen():
	for a in range(screen_y):
		game_screen.append([])
	for a in range(screen_y):
		for b in range(screen_x):
			game_screen[a].append(filler)

#copy icons from game_map into game_screen
def update_screen():
	for a in range(screen_y):
		for b in range(screen_x):
			game_screen[a][b] = game_map[a + camera_y][b + camera_x][0][1]

#displays the array game_screen in the terminal
def draw_screen():
	for a in range(screen_y):
		for b in range(screen_x):
			if (a + 1) < screen_y or (b + 1) < screen_x:
				screen.addstr(game_screen[a][b])
			else:
				screen.insstr(game_screen[a][b])

#add object to game_map
def make_object(name, icon, y, x):
	if game_map[y][x][0][0] == "filler":
		game_map[y][x][0] = [name, icon]
	else:
		game_map[y][x].insert(0, [name, icon])

#make random objects; will only place objects in empty cells
def make_rand_objects(amount, name, icon, min_y, min_x, max_y, max_x):
	counter = 0
	if (max_y - min_y + 1) * (max_x - min_x + 1) < amount:
		counter = amount
	while counter < amount:
		coords = [random.randrange(min_y, max_y), random.randrange(min_x, max_x)]
		if game_map[coords[0]][coords[1]][0][0] == "filler":
			game_map[coords[0]][coords[1]][0] = [name, icon]
			counter += 1

#returns an array of all locations of object in game_map
def find_object(name):
	result = []
	for a in range(map_y):
			for b in range(map_x):
				if game_map[a][b][0][0] == name:
					result.append([a, b])
	return result

#does collision handling and moves the player accordingly
def move_player(move_y, move_x):
		y, x, = find_object("player")[0]
		new_y = y + move_y
		new_x = x + move_x
		if new_y >= camera_y and new_y <= camera_y + screen_y - 1 and new_x >= camera_x and new_x <= camera_x + screen_x - 1:
			if not game_map[new_y][new_x][0][0] == "wall":
				if len(game_map[y][x]) == 1:
					game_map[y][x][0] = ["filler", filler]
				else:
					del(game_map[y][x][0])
				make_object("player", player_icon, new_y, new_x)

#startup functions
def game_startup():
	global game_state
	make_map()
	make_screen()
	make_object("player", player_icon, player_y, player_x)
	make_rand_objects(200, "wall", wall_icon, camera_y, camera_x, screen_y, screen_x)
	make_rand_objects(20, "door", door_icon, camera_y, camera_x, screen_y, screen_x)
	game_state = "game_loop"

#handles input and basic movement logic
def input_logic():
	global game_state

	#keyboard addresses
	escape = 27
	down = 258
	up = 259
	left = 260
	right = 261
	w = 119
	a = 97
	s = 115
	d = 100
	space = 32

	key = screen.getch()

	#exits game
	if key == escape:
		game_state = "quit_game"

	#controls character
	elif key == w:
		move_player(-1, 0)
	elif key == s:
		move_player(+1, 0)
	elif key == a:
		move_player(0, -1)
	elif key == d:
		move_player(0, +1)

	#controls camera
	elif key == up:
		var = 1
	elif key == down:
		var = 1
	elif key == left:
		var = 1
	elif key == right:
		var = 1

#this is the game loop
def game_loop():
	global game_state
	while game_state == "game_loop":
		screen.erase()
		update_screen()
		draw_screen()
		input_logic()

#this is the main loop
game_state = "game_startup"
while True:
	if game_state == "game_startup":
		game_startup()
	if game_state == "game_loop":
		game_loop()
	else:
		break

#exits curses and quits game
screen.keypad(False)
curses.echo()
curses.endwin()








































