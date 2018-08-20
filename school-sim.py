"""
To Do List:
	1. create center camera function 
	2. create procedural generation function
	3. create NPCs
	4. make border wall fancier
	5. put game object icons into a dictionary
	6. create is object onscreen function
"""

#imported modules
import curses
import random
import time

#curses setup
screen = curses.initscr()
screen.keypad(True)
#screen.timeout(25)
curses.noecho()
curses.curs_set(False)

#misc variables
map_y = 75
map_x = 250
screen_y, screen_x = screen.getmaxyx()
camera_max_y = map_y - screen_y
camera_max_x = map_x - screen_x
camera_y = 0
camera_x = 0
camera_speed = 5
camera_buffer_y = screen_y/4
camera_buffer_x = screen_x/4
collision_objects = ["wall", "border"]

#main arrays
game_map = []
game_screen = []
ui_screen = []

#game object icons
game_icons = {"filler" : " ",
			  "player" : "@", 
			  "door" : "▒",
			  "wall" : "█"}

#make the array game_map and fill it with filler arrays
def make_map():
	for a in range(map_y):
		game_map.append([])
	for a in range(map_y):
		for b in range(map_x):
			game_map[a].append([["filler", game_icons["filler"]]])

#make the array game_screen and fill it with filler
def make_screen():
	for a in range(screen_y):
		game_screen.append([])
	for a in range(screen_y):
		for b in range(screen_x):
			game_screen[a].append(game_icons["filler"])

#copy icons from game_map into game_screen
def update_screen():
	for a in range(screen_y):
		for b in range(screen_x):
			if a < map_y and b < map_x:
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
def make_object(name, icon, y, x, replaceable_objects = ["filler"]):
	if game_map[y][x][0][0] in replaceable_objects:
		game_map[y][x][0] = [name, icon]
	else:
		game_map[y][x].insert(0, [name, icon])

#make random objects; will only place objects in empty cells
def make_rand_objects(amount, name, icon, min_y, min_x, max_y, max_x, allowed_cells = ["filler"]):
	
	#keeps everything within the game_map
	min_y = max(0, min_y)
	min_x = max(0, min_x)
	max_y = min(map_y, max_y)
	max_x = min(map_x, max_x)
	
	#fills every space and bypasses randomness if amount > available_cells
	counter = 0
	available_cells = 0
	for a in range(min_y, max_y):
		for b in range(min_x, max_x):
			if game_map[a][b][0][0] in allowed_cells:
				available_cells += 1
	if amount >= available_cells:
		for a in range(min_y, max_y):
			for b in range(min_x, max_x):
				if game_map[a][b][0][0] in allowed_cells:
					make_object(name, icon, a, b)
		counter = amount
			
	#adds the objects to game_map
	while counter < amount:
		coords = [random.randrange(min_y, max_y), random.randrange(min_x, max_x)]
		if game_map[coords[0]][coords[1]][0][0] in allowed_cells:
			make_object(name, icon, coords[0], coords[1], replaceable_objects = allowed_cells)
			counter += 1

#returns an array of all locations of object in game_map
def find_object(name):
	result = []
	for a in range(map_y):
			for b in range(map_x):
				if game_map[a][b][0][0] == name:
					result.append([a, b])
	return result

#does collision handling and moves the player and camera accordingly
def move_player(move_y, move_x):
	y, x, = find_object("player")[0]
	new_y = y + move_y
	new_x = x + move_x
	if new_y >= 0 and new_y <= map_y - 1 and new_x >= 0 and new_x <= map_x - 1:
		if not game_map[new_y][new_x][0][0] in collision_objects:
			if len(game_map[y][x]) == 1:
				game_map[y][x][0] = ["filler", game_icons["filler"]]
			else:
				del(game_map[y][x][0])
			make_object("player", game_icons["player"], new_y, new_x)

			#adjusts camera
			if on_screen("player"):
				adjust = False
				if new_y - camera_buffer_y < camera_y and move_y < 0:
					adjust = True
				elif new_y + camera_buffer_y > camera_y + screen_y - 1 and move_y > 0:
					adjust = True
				if new_x - camera_buffer_x < camera_x and move_x < 0:
					adjust = True
				elif new_x + camera_buffer_x > camera_x + screen_x - 1 and move_x > 0:
					adjust = True
				if adjust:
					move_camera(move_y, move_x)
			else:
				center_camera()

#checks boundaries and moves the camera accordingly
def move_camera(move_y, move_x):
	global camera_y
	global camera_x
	new_y = int(camera_y + move_y)
	new_x = int(camera_x + move_x)
	if move_y < 0:
		camera_y = max(0, new_y)
	else:
		camera_y = min(camera_max_y, new_y)
	if move_x < 0:
		camera_x = max(0, new_x)
	else:
		camera_x = min(camera_max_x, new_x)

#centers camera on player
def center_camera():
	global camera_y
	global camera_x
	camera_y, camera_x, = find_object("player")[0]
	move_camera(-12, -40)

#builds a border wall
def make_border_wall():
	for a in range(map_y):
		make_object("border", game_icons["wall"], a, 0)
		make_object("border", game_icons["wall"], a, map_x - 1)
	for a in range(map_x):
		make_object("border", game_icons["wall"], 0, a)
		make_object("border", game_icons["wall"], map_y - 1, a)

#startup functions
def game_startup():
	global game_state
	make_map()
	make_screen()
	make_border_wall()
	make_object("player", game_icons["player"], 4, 4)
	make_rand_objects(100, "wall", game_icons["wall"], 0, 0, map_y, map_x)
	make_rand_objects(50, "door", game_icons["door"], 0, 0, map_y, map_x, ["filler", "wall"])
	game_state = "game_loop"

#handles input and basic movement logic
def input_logic():
	global game_state
	global camera_y
	global camera_x

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
		move_camera(-camera_speed, 0)
	elif key == down:
		move_camera(camera_speed, 0)
	elif key == left:
		move_camera(0, -camera_speed)
	elif key == right:
		move_camera(0, camera_speed)

#returns true if object is in game_screen
def on_screen(object):
	icon = game_icons[object]
	for a in range(screen_y):
		for b in range(screen_x):
			if game_screen[a][b] == icon:
				return True
	return False

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
