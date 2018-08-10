import curses

screen = curses.initscr()
screen.keypad(True)
screen.timeout(25)
curses.noecho()
curses.curs_set(False)

screen_y, screen_x = screen.getmaxyx()

#view = [["1", "2", "3"], ["a", "b", "c"]]
view = [[]]

for a in range(screen_y):
	view.append([])

for a in range(screen_y):
	for b in range(screen_x):
		view[a].append("#")

#screen.addstr(str(len(view)))
#screen.addstr("---")
#screen.addstr(str(len(range(80))))

for a in range(screen_y):
	for b in range(screen_x):
		screen.insch(view[a][b])

while True:
	screen.insch("g")
	key = screen.getch()
	if key == 27:
		break

screen.keypad(False)
curses.echo()
curses.endwin()
