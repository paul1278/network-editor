import curses
import math
from utils import *
import config
config.load()

mainwin = None
mainwin_inner = None
commandwin = None
activewin = None
stdwin = None
def start(stdscr):
    global mainwin, mainwin_inner, commandwin, activewin, stdwin
    stdwin = stdscr
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
    mainwin = curses.newwin(height, width, begin_y, begin_x)
    mainwin.box()
    mainwin.refresh()

    mainwin_inner = curses.newwin(height - 3, width - 4, begin_y + 1, begin_x + 2)
    mainwin_inner.addstr(1,1, "\u001b[32m[+]\u001b[0m")
    mainwin_inner.refresh()

    commandwin = curses.newwin(5, dims[1], height, 0)
    commandwin.addstr(2,2, "> ")
    commandwin.box()
    commandwin.refresh()

    _height = math.floor((height - 5) / 2)
    
    activewin = curses.newwin(_height, dims[1] - width, 0, width)
    activewin.box()
    activewin.refresh()
    printActiveFilters()
    win4 = curses.newwin(height - _height, dims[1] - width, _height, width)
    win4.box()
    win4.refresh()
    inputLoop()

def inputLoop():
    k = 0
    _input_ = ""
    # Loop where k is the last character pressed
    while (k != '\n'):

        # Wait for next input
        k = stdwin.getkey()
        if(k == "\n"):
            break
        _input_ += str(k)

        # Refresh the screen
        commandwin.addstr(2,4, _input_)
        commandwin.refresh()
    
    mainwin_inner.clear()
    if _input_ == "filters":
        mainwin_inner.addstr(0,0, "")
    elif _input_ == "help":
        printHelp()
    elif _input_[0:3] == "ef ":
        enableFilter(_input_[3:])
    else:
        mainwin_inner.addstr(0,0, "Dont know that command!")
    mainwin_inner.refresh()
    k = ''
    commandwin.clear()
    commandwin.addstr(2,2, "> ")
    commandwin.box()
    _input_ = ""
    commandwin.refresh()
    inputLoop()

def printActiveFilters():
    activewin.addstr(1, 2, "Active filters:")
    for i,f in enumerate(config.filters):
        activewin.addstr(i + 2, 2, "- " + f)
    activewin.refresh()

def main():
    curses.wrapper(start)

def printHelp():
    mainwin_inner.addstr(0,0, 'Help')
    mainwin_inner.addstr(1,0, 'In the following you can see all available commands.')
    cmds = [
        "filters \tShow all filters"
    ]
    for i,f in enumerate(cmds):
        mainwin_inner.addstr(i + 3, 0, f)

def enableFilter(name):
    filter = config.filters.get(name, None)
    if filter == None:
        mainwin_inner.addstr(0,0, 'Error! Cannot find filter with name ' + name, curses.color_pair(2))

if __name__ == "__main__":
    main()