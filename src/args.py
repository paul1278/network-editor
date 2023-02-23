import argparse
args = None


def argParser():
    global args
    if args == None:
        parser = argparse.ArgumentParser(
                        prog = 'start.py')
        parser.add_argument('-w', '--workspace', help="Give a path to a ready workspace")
        parser.add_argument('-i', "--interactive", action='store_true', help="Start with a UI")
        parser.add_argument('-v', '--verbose', action='store_true', help="Enable debug mode without config")
        args = parser.parse_args()
        
    return args