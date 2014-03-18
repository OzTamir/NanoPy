#!/usr/bin/env python
import time
import curses
from curses.textpad import Textbox, rectangle
import sys
from file_util import save, read_file

# Key bindings
bindings = {'^X' : 'Exit'}

def exit(stdscr, win, data, filename=None):
	write_h = curses.LINES - 3
	msg = 'Save modified buffer (ANSWERING "No" WILL DESTROY CHANGES) ?'
	msg += ' ' * (curses.COLS - len(msg))
	stdscr.addstr(write_h, 0, msg, curses.A_REVERSE)
	write_h += 1
	stdscr.addstr(write_h, 0, ' Y', curses.A_REVERSE)
	stdscr.addstr(write_h, 3, 'Yes')
	write_h += 1
	stdscr.addstr(write_h, 0, ' N', curses.A_REVERSE)
	stdscr.addstr(write_h, 3, 'No')
	stdscr.refresh()
	while True:
		char = win.getkey()
		if char == 'N' or char == 'n':
			return 0
		if char == 'Y' or char == 'y':
			return save(stdscr, data, filename)

def add_head(stdscr, filename='New Buffer'):
	title = 'GNU nano 2.0.6'
	background = ' ' * ((curses.COLS - len(title)) / 3)
	title = ''.join([title, background, filename])
	title += ' ' * (curses.COLS - len(title))
	stdscr.addstr(0, 0, title, curses.A_REVERSE)
	stdscr.refresh()

def write_keys(stdscr):
	global bindings
	write_h = curses.LINES - 3
	write_w = 0
	stdscr.move(write_h, write_w)
	stdscr.clrtobot()
	for key, value in bindings.items():
		if write_h + len(key) + len(value) > curses.COLS:
			write_h += 1
			write_w = 0
		stdscr.addstr(write_h, write_w, key, curses.A_REVERSE)
		write_w += len(key)
		stdscr.addstr(write_h, write_w, ' ' + value + ' ')
		write_w += len(value) + 2
	stdscr.refresh()

def main(stdscr, data=None):
	if data:
		add_head(stdscr, data)
	else:
		add_head(stdscr)
	write_keys(stdscr)
	editwin = curses.newwin(curses.LINES - 6, curses.COLS - 3, 2, 1)
	rectangle(stdscr, 1,0, curses.LINES - 4, curses.COLS - 1)
	stdscr.refresh()
	pos_h = 0
	pos_w = 0
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
	while True:
		char = editwin.getkey()
		# CTRL^X
		if ord(char) == 24:
			ret = exit(stdscr, editwin, data, filename)
			if ret == 0:
				curses.echo()
				curses.endwin()
				sys.exit(0)
			else:
				write_keys(stdscr)
				continue
		data += char
		if char == '\n':
			pos_h += 1
			pos_w = 0
			editwin.move(pos_h, 0)
			stdscr.refresh()
			continue
		editwin.addch(pos_h, pos_w, char)
		if pos_w == curses.COLS - 4:
			pos_h += 1
			pos_w = 0
			editwin.move(pos_h, 0)
			stdscr.refresh()
		else:
			pos_w += 1
		editwin.refresh()

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
	except Exception, e:
		print e
	finally:
		curses.nocbreak()
		stdscr.keypad(False)
		curses.echo()
		curses.endwin()