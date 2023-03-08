#!/usr/local/bin/python3
from utils import *
import config
import main
import args
import workspace
import ui


if __name__ == "__main__":
    # Print the application ASCII-header (very important!)
    print_header()
    if config.load() == False:
        error("Config not loadable - program terminated")
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
        ui.prgm()
    else:    
        main.start_bridge(None)