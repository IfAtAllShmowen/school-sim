#imported modules
import curses

#curses setup
screen = curses.initscr()
screen.keypad(True)
screen.timeout(2500)
curses.noecho()
curses.curs_set(False)

#misc variables
screen_y, screen_x = screen.getmaxyx()
view_screen = [[]]
filler = " "
down = 258
up = 259
left = 260
right = 261
player = ["@", 4, 4]

#makes the array view_screen and fills it with filler
def make_screen():
	global view_screen
	view_screen = [[]]
	for a in range(screen_y):
		view_screen.append([])
	for a in range(screen_y):
		for b in range(screen_x):
			view_screen[a].append(filler)

#displays the array view_screen in the terminal
def draw_screen():
	for a in range(screen_y):
		for b in range(screen_x):
			if a < screen_y - 1 or b < screen_x -1:
				screen.addch(view_screen[a][b])
			else:
				screen.insch(view_screen[a][b])

#this is the main loop
make_screen()
while True:
	view_screen[player[1]][player[2]] = player[0]
	screen.clear()
	draw_screen()
	key = screen.getch()
	if key == 27:
		break
	elif key == down:
		if player[1] < screen_y - 1:
			view_screen[player[1]][player[2]] = filler
			player[1] += 1
	elif key == up:
		if player[1] > 0:
			view_screen[player[1]][player[2]] = filler
			player[1] -= 1
	elif key == left:
		if player[2] > 0:
			view_screen[player[1]][player[2]] = filler
			player[2] -= 1
	elif key == right:
		if player[2] < screen_x - 1:
			view_screen[player[1]][player[2]] = filler
			player[2] += 1

#exits curses
screen.keypad(False)
curses.echo()
curses.endwin()

