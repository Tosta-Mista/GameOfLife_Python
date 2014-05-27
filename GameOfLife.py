#!/bin/python
#-*-- coding: utf-8 -*-
import curses


def init_curses(width=20, height=20, pos=(0, 0)):
    """
    init_curses() :
    This function initialise the border and the "window" into the terminal
    """
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    window = curses.newwin(width + 2, height + 2, pos[0], pos[1])
    window.border(0)
    window.keypad(1)
    return window


def close_curses():
    """
    close_curses() :
    This function set how to close the "window" into the terminal
    """
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()


def initialize(config=None, width=20, height=20):
    """
    initialize() :
    This function init the GameofLife
    """
    space = [[0 for col in range(width)] for row in range(height)]
    for row, col in config:
        space[row][col] = 1
    return space


def display(space, win):
    """
    display() :
    This function set how to display the values.
    """
    for nline, line in enumerate(space):
        for ncell, cell in enumerate(line):
            if cell == 0:
                win.addstr(nline + 1, ncell + 1, '.')
            else:
                win.addstr(nline + 1, ncell + 1, '*')


def neighbours(space, row, col):
    """
    neighbours() :
    Main function to calculate the neighbours
    """
    max_border_row = len(space) - 1
    max_border_col = len(space[0]) - 1

    def neighbour(row, col):
        if row == -1:
            row = max_border_row
        elif row > max_border_row:
            row = 0
        if col == -1:
            col = max_border_col
        elif col > max_border_col:
            col = 0

        return space[row][col]

    return neighbour(row, col - 1) + neighbour(row - 1, col - 1) + neighbour(row - 1, col) + \
           neighbour(row - 1, col + 1) + neighbour(row, col + 1) + neighbour(row + 1, col + 1) + \
           neighbour(row, +1, col) + neighbour(row + 1, col - 1)


def transition(space, width=20, height=20):
    """
    transition() :
    Parse the matrix set if the cell is on "born" state, "survive" state and "dead" state and return updated matrix.
    """
    space_next = [[0 for col in range(width)] for row in range(height)]
    for row in range(height):
        for col in range(width):
            n = neighbours(space, row, col)
            if space[row][col] == 0 and n == 3:
                space_next[row][col] = 1
            elif space[row][col] == 1 and (n == 2 or n ==3):
                space_next[row][col] = 1
    return space_next


if __name__ == "__main__":
    # Cell
    u = ((8, 8), (8, 19), (9, 8), (9, 10), (10, 8), (10, 9), (10, 10))

    win = init_curses()
    space = initialize(u)
    # Running Loop the user can quit the using "escape" key (ASCII 27)
    while True:
        display(space, win)
        key = win.getch()
        if key == 27:
            break
        space = transition(space)
    close_curses()