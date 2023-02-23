import sys
debug = False

loggingFunc = print

def ansiColor(color):
  if(loggingFunc != print):
    return ""
  if(color == "reset"):
    return "\u001b[0m"
  elif(color == "green"):
    return "\u001b[32m"
  elif(color == "blue"):
    return "\u001b[34m"
  elif(color == "red"):
    return "\u001b[31m"

def ok(*args):
  loggingFunc("{}[+]{}".format(colorFunc("green"),colorFunc("reset")), *args)

def error(*args):
  loggingFunc("{}[-]{}".format(colorFunc("red"),colorFunc("reset")), *args)

def isUI():
  return len(sys.argv) > 1 and sys.argv[1] == "-i"

def debug(*args):
  if debug:
    loggingFunc("{}[*]{}".format(colorFunc("blue"),colorFunc("reset")), *args)

def print_header():
  print(''' (   (                                                 
 )\ ))\ )         )                          )         
(()/(()/(      ( /(  (  (         (       ( /(    (    
 /(_))(_))(    )\())))\ )(   (   ))\`  )  )\())(  )(   
(_))(_))  )\ )(_))//((_|()\  )\ /((_)(/( (_))/ )\(()\  
| _ \_ _|_(_/(| |_(_))  ((_)((_|_))((_)_\| |_ ((_)((_) 
|  _/| || ' \))  _/ -_)| '_/ _|/ -_) '_ \)  _/ _ \ '_| 
|_| |___|_||_| \__\___||_| \__|\___| .__/ \__\___/_|   
                                   |_|                 ''')
  ok("Starting up")

def set_debug(v):
  global debug
  debug = v

def setLoggingFunc(v):
  global loggingFunc
  loggingFunc = v

colorFunc = ansiColor