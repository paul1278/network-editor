import sys,os
import curses
import math
from utils import *
import config
config.load()
def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    dims = stdscr.getmaxyx()
    begin_x = 0; begin_y = 0
    height = dims[0] - 5
    width = math.floor(dims[1] / 3 * 2)
    win = curses.newwin(height, width, begin_y, begin_x)
    win.box()
    win.refresh()

    win_inner = curses.newwin(height - 4, width - 4, begin_y + 2, begin_x + 2)
    win_inner.addstr(1,1, "\u001b[32m[+]\u001b[0m")
    win_inner.refresh()

    win2 = curses.newwin(5, dims[1], height, 0)
    win2.addstr(2,2, "> ")
    win2.box()
    win2.refresh()

    _height = math.floor((height - 5) / 2)
    
    win3 = curses.newwin(_height, dims[1] - width, 0, width)
    win3.box()
    win3.refresh()

    win4 = curses.newwin(height - _height, dims[1] - width, _height, width)
    win4.box()
    win4.refresh()
    _input_ = ""
    while True:
        # Loop where k is the last character pressed
        while (k != '\n'):

            # Wait for next input
            k = stdscr.getkey()
            if(k == "\n"):
                break
            _input_ += str(k)

            # Refresh the screen
            win2.addstr(2,4, _input_)
            win2.refresh()
        
        win_inner.clear()
        if _input_ == "filters":
            win_inner.addstr(0,0, "\n".join(list(config.data)))
        else:
            win_inner.addstr(0,0, "Dont know that command!")
        win_inner.refresh()
        k = ''
        win2.clear()
        win2.addstr(2,2, "> ")
        win2.box()
        _input_ = ""
        win2.refresh()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()