#!/usr/bin/env python
from __future__ import print_function
import time
import curses
from curses.textpad import Textbox, rectangle
import sys
from file_util import save, read_file
from cli import modified_alert, add_head, write_keys, init_term

def exit(stdscr, win, data, filename=None):
	'''Called when CTRL^X is being pressed, prompts the user to save changes'''
	# Set position for writing
	write_h = curses.LINES - 3
	# Compile the message to the user
	msg = 'Save modified buffer (ANSWERING "No" WILL DESTROY CHANGES) ?'
	msg += ' ' * (curses.COLS - len(msg))
	# Add it
	stdscr.addstr(write_h, 0, msg, curses.A_REVERSE)
	write_h += 1
	# Add all the options
	stdscr.addstr(write_h, 0, ' Y', curses.A_REVERSE)
	stdscr.addstr(write_h, 3, 'Yes')
	write_h += 1
	stdscr.addstr(write_h, 0, ' N', curses.A_REVERSE)
	stdscr.addstr(write_h, 3, 'No')
	stdscr.refresh()
	# Get the user's selection
	while True:
		char = win.getkey()
		# If it's a No, return a 0 exit code
		if char == 'N' or char == 'n':
			return 0
		# If the user want to save' do so
		if char == 'Y' or char == 'y':
			return save(stdscr, data, filename)

def main(stdscr, data=None):
	'''Main function, includes the input-output loop'''
	# Fire up the CLI and set everything up
	init_term(stdscr, data)
	# Initial cursor positions
	pos_h = 0
	pos_w = 0
	# If we're opening a file, add it's content to the view
	if data:
		filename = data
		data = read_file(data)
		editwin.addstr(data)
		pos_h = len(data.split('\n'))
		pos_w = len(data) - pos_h
	else:
		filename = None
		data = ''
	stdscr.refresh()
	modified = False
	# Main editing loop
	while True:
		# Get input from user
		char = editwin.getkey()
		
		# CTRL^X
		if ord(char) == 24:
			if modified:
				ret = exit(stdscr, editwin, data, filename)
			else:
				ret = 0
			if ret == 0:
				curses.echo()
				curses.endwin()
				sys.exit(0)
			else:
				write_keys(stdscr)
				continue

		# Scrolling feature - SEMI-WORKING, NEED MORE WORK
		if pos_h >= curses.LINES - 7:
			stdscr.scroll()
			pos_h -= 1
			stdscr.refresh()
		if char == '\n':
			pos_h += 1
			pos_w = 0
			editwin.move(pos_h, 0)
			stdscr.refresh()
			continue

		# Backspace
		if ord(char) == 8 or ord(char) == 127:
			# If we are at the first char, we ignore the click since there's nothing to delete
			if pos_h == 0 and pos_w == 0:
				continue
			# Else, if we delete a line we need to find the position of the last character typed
			if pos_w == 0:
				pos_w = curses.COLS - 2
				while pos_w != 0:
					pos_w -= 1
					try:
						c = chr(editwin.inch(pos_h - 1, pos_w))
						if c != ' ':
							pos_w += 1
							break
					except Exception:
						continue
				pos_h -= 1
				editwin.move(pos_h, pos_w)
				editwin.refresh()
				continue
			# Else, just remove the char and move the cursor position
			else:
				editwin.delch(pos_h, pos_w - 1)
				pos_w -= 1
				stdscr.refresh()
				continue
		
		# Add recived input to data buffer and add it to view
		data += char
		editwin.addch(pos_h, pos_w, char)

		# Deal with the size limits
		if pos_w == curses.COLS - 4:
			pos_h += 1
			pos_w = 0
			editwin.move(pos_h, 0)
			stdscr.refresh()
		else:
			pos_w += 1
		
		# Finally, refresh the view
		editwin.refresh()

		# We keep a boolean value to add the 'Modified' label when we make changes
		if not modified:
			modified = True
			modified_alert(stdscr)

if __name__ == '__main__':
	stdscr = curses.initscr()
	curses.noecho()

	if len(sys.argv) == 2:
		if sys.argv[1] != '-d':
			main(stdscr, sys.argv[1])
		# Debug mode - display exception if raised
		else:
			main(stdscr)
	try:
		main(stdscr)
	finally:
		curses.nocbreak()
		stdscr.keypad(False)
		curses.echo()
		curses.endwin()