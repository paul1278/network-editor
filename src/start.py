import curses
import math
from utils import *
import config
import main
import args
import workspace

mainwin = None
mainwin_inner = None
commandwin = None
activewin = None
stdwin = None

head = ''' (   (                                                 
 )\ ))\ )         )                          )         
(()/(()/(      ( /(  (  (         (       ( /(    (    
 /(_))(_))(    )\())))\ )(   (   ))\`  )  )\())(  )(   
(_))(_))  )\ )(_))//((_|()\  )\ /((_)(/( (_))/ )\(()\  
| _ \_ _|_(_/(| |_(_))  ((_)((_|_))((_)_\| |_ ((_)((_) 
|  _/| || ' \))  _/ -_)| '_/ _|/ -_) '_ \)  _/ _ \ '_| 
|_| |___|_||_| \__\___||_| \__|\___| .__/ \__\___/_|   
                                   |_|                 '''

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

    mainwin_inner = curses.newwin(height - 2, width - 4, begin_y + 1, begin_x + 2)
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
    lines = head.splitlines()
    dims4 = win4.getmaxyx()
    for i in range(len(head.splitlines())):
        line = lines[i]
        try:
            win4.addstr(i + 2, math.floor((dims4[1] - len(line)) / 2), line)
        except:
            break
    win4.refresh()
    while True:
        inputLoop()

def inputLoop():
    k = 0
    _input_ = ""
    mlen = 0
    # Loop where k is the last character pressed
    while (k != '\n'):

        # Wait for next input
        k = stdwin.getkey()
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
    activewin.addstr(1, 2, "Active filters:")
    for i,f in enumerate(workspace.filters):
        activewin.addstr(i + 2, 2, "- " + f + " [" + ("ENABLED" if workspace.filters[f].enabled else "DISABLED") + "]" + " (triggers: " + ", ".join(workspace.filters[f].actions) + ")")
    activewin.refresh()

def prgm():
    curses.wrapper(start)

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
    workspace.enableFilter(name)
    printActiveFilters()

def disableFilter(name):
    filter = workspace.filters.get(name, None)
    if filter == None:
        mainwin_inner.addstr(0,0, 'Error! Cannot find filter with name ' + name, curses.color_pair(2))
    workspace.disableFilter(name)
    printActiveFilters()

if __name__ == "__main__":
    print_header()
    if config.load() == False:
        error("Program terminated")
        quit(1)
    
    setDebug(args.argParser().verbose)

    ws = args.argParser().workspace
    if(ws == None):
        error("Specify a workspace using -w")
        sys.exit(1)
    ok("Loading workspace", ws)
    if workspace.loadWorkspace(ws):
        ok("Loaded workspace", ws)
    else:
        error("Cannot load workspace under", ws, "- is it really a workspace?")
        sys.exit(1)
    
    if args.argParser().interactive:
        ok("Starting interactive UI mode")
        prgm()
    else:    
        main.start_bridge(None)