import curses

def save(stdscr, data, filename=None):
	'''Save the data buffer to a file'''
	# If the user is creating a new file, ask him for a name
	if filename is None:
		write_h = curses.LINES - 3
		msg = 'File Name to Write: '
		write_w = len(msg) + 1
		msg += ' ' * (curses.COLS - len(msg))
		stdscr.addstr(write_h, 0, msg, curses.A_REVERSE)
		write_h += 1
		stdscr.addstr(write_h, 0, ' ENTER', curses.A_REVERSE)
		stdscr.addstr(write_h, 7, 'Save')
		write_h += 1
		stdscr.addstr(write_h, 0, ' ^C', curses.A_REVERSE)
		stdscr.addstr(write_h, 3, 'Cancel')
		stdscr.move(write_h - 2, write_w)
		curses.echo()
		stdscr.refresh()
	# If the user is happy with the changes, save it to file.
	# If he regrets, return to the editing view
	try:
		if filename is None:
			filename = stdscr.getstr().decode(encoding="utf-8")
		with open(filename, 'w+') as file:
			file.write(data)
		return 0
	except KeyboardInterrupt:
		return 1

def read_file(filename):
	'''Return the content of a file'''
	with open(filename, 'r') as file:
		return file.read()