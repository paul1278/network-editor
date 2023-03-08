import curses, sys
import math
import workspace
import main
import utils

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

    # Calc main window, will be 2/3 width
    dims = stdscr.getmaxyx()
    
    if dims[0] < 20 or dims[1] < 104:
        raise(Exception("Window must be > 20 in height (is " + str(dims[0]) + ") and > 104 in width (is " + str(dims[1]) + ")"))

    begin_x = 0; begin_y = 0
    height = dims[0] - 5
    width = math.floor(dims[1] / 3 * 2)
    mainwin = curses.newwin(height, width, begin_y, begin_x)
    mainwin.box()
    mainwin.refresh()

    # Make an inner window for padding.
    mainwin_inner = curses.newwin(height - 2, width - 4, begin_y + 1, begin_x + 2)
    mainwin_inner.refresh()

    # Make the command window
    commandwin = curses.newwin(5, dims[1], height, 0)
    commandwin.addstr(2,2, "> ")
    commandwin.box()
    commandwin.refresh()
    

    activewinContainer = curses.newwin(height -3, dims[1] - width, 0, width)
    activewinContainer.box()
    activewinContainer.refresh()
    activewin = curses.newwin(height -5, dims[1] - width -2, 1, width + 1)
    printActiveFilters()

    win4 = curses.newwin(3, dims[1] - width, height - 3, width)
    win4.box()
    win4.addstr(1, 2, "pinterceptor v1.0.0")
    win4.refresh()
    while True:
        inputLoop()

def inputLoop():
    k = 0
    _input_ = ""
    # Loop where k is the last character pressed
    while (k != '\n'):

        # Wait for next input
        try:
            k = stdwin.getkey()
        except KeyboardInterrupt:
            sys.exit(0)
        
        if(k == "\n"):
            break
        if(len(k) > 1):
            # Special key
            if k == "KEY_BACKSPACE":
                _input_ = _input_[0:-1]
            else:
                continue
        else:
            _input_ += str(k)

        # Refresh the screen
        commandwin.addstr(2,4, _input_)
        commandwin.refresh()
    
    mainwin_inner.clear()
    if _input_ == "help":
        printHelp()
    elif _input_ == "eb":
        main.start_bridge(mainwin_inner)
    elif _input_ == "reload":
        workspace.reload()
    elif _input_[0:3] == "ef ":
        enableFilter(_input_[3:].strip())
    elif _input_[0:3] == "df ":
        disableFilter(_input_[3:].strip())
    else:
        mainwin_inner.addstr(0,0, "Dont know that command!")
    mainwin_inner.refresh()
    k = ''
    commandwin.clear()
    commandwin.addstr(2,2, "> ")
    commandwin.box()
    _input_ = ""
    commandwin.refresh()

def printActiveFilters():
    activewin.clear()
    activewin.addstr(0, 1, "Active filters:")
    for i,f in enumerate(workspace.filters):
        activewin.addstr(i + 1, 1, "- " + f + " [" + ("ENABLED" if workspace.filters[f].enabled else "DISABLED") + "]" + " (" + ", ".join(workspace.filters[f].actions) + ")")
    activewin.refresh()

def prgm():
    try:
        curses.wrapper(start)
    except Exception as e:
        utils.error(e)

def printHelp():
    mainwin_inner.addstr(0,0, 'Help')
    mainwin_inner.addstr(1,0, 'In the following you can see all available commands.')
    cmds = [
        "eb \t\tEnable bridge (Stop with CTRL+c again)",
        "ef <filter>\tEnable filter",
        "df <filter>\tDisable filter",
        "reload\t\tReload workspace code"
    ]
    for i,f in enumerate(cmds):
        mainwin_inner.addstr(i + 3, 0, f)

def enableFilter(name):
    filter = workspace.filters.get(name, None)
    if filter == None:
        mainwin_inner.addstr(0,0, 'Error! Cannot find filter with name ' + name, curses.color_pair(2))
    else:
        workspace.enableFilter(name)
        printActiveFilters()

def disableFilter(name):
    filter = workspace.filters.get(name, None)
    if filter == None:
        mainwin_inner.addstr(0,0, 'Error! Cannot find filter with name ' + name, curses.color_pair(2))
    else:
        workspace.disableFilter(name)
        printActiveFilters()