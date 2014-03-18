import curses
from curses.textpad import rectangle


# Key bindings
bindings = {'^X' : 'Exit'}

def modified_alert(stdscr):
	'''Add a 'Modified' label when the user made changes to the buffer'''
	alert = 'Modified   '
	write_w = curses.COLS - len(alert)
	stdscr.addstr(0, write_w, alert, curses.A_REVERSE)
	stdscr.refresh()

def add_head(stdscr, filename='New Buffer'):
	'''Add the title string for the CLI'''
	title = 'NanoPy 1.0.1'
	background = ' ' * ((curses.COLS - len(title)) // 3)
	title = ''.join([title, background, filename])
	title += ' ' * (curses.COLS - len(title))
	stdscr.addstr(0, 0, title, curses.A_REVERSE)
	stdscr.refresh()

def write_keys(stdscr):
	'''Add the current key bindings to the bottom of the screen'''
	global bindings
	write_h = curses.LINES - 3
	write_w = 0
	stdscr.move(write_h, write_w)
	stdscr.clrtobot()
	# For each key, add it to the view
	for key, value in bindings.items():
		if write_h + len(key) + len(value) > curses.COLS:
			write_h += 1
			write_w = 0
		stdscr.addstr(write_h, write_w, key, curses.A_REVERSE)
		write_w += len(key)
		stdscr.addstr(write_h, write_w, ' ' + value + ' ')
		write_w += len(value) + 2
	stdscr.refresh()

def init_term(stdscr, data=None):
	'''Initialize the terminal UI for NanoPy'''
	if data:
		add_head(stdscr, data)
	else:
		add_head(stdscr)
	write_keys(stdscr)
	editwin = curses.newwin(curses.LINES - 6, curses.COLS - 3, 2, 1)
	rectangle(stdscr, 1, 0, (curses.LINES - 4), (curses.COLS - 1))
	stdscr.scrollok(True)
	stdscr.refresh()
	return editwin