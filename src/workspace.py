import yaml
from yaml.loader import SafeLoader
from utils import *
from os.path import isdir
import sys
from importlib import reload as mreload  # Python 3.4+

data = None
protocols = {}
filters = {}
actions = {}
currentWorkspacePath = None

def isWorkspace(path):
  if isdir(path):
    if isdir(path + "/protocols") and isdir(path + "/actions") and isdir(path + "/filter"):
      return True
  return False

def reload():
  if currentWorkspacePath == None:
    return False
  loadWorkspace(currentWorkspacePath)

def loadWorkspace(path):
  global data, currentWorkspacePath
  if not isWorkspace(path):
    return False
  currentWorkspacePath = path
  try:
    sys.path.index(path)
  except:
    sys.path.append(path)

  try:
    # Open the file and load the file
    with open(path + '/workspace.yaml') as f:
      data = yaml.load(f, Loader=SafeLoader)
      loadProtocols()
      loadActions()
      loadFilter()
      checkInterfaces()
      return True
  except FileNotFoundError:
    error("Config file was not found!")
    return False
  except yaml.constructor.ConstructorError as e:
    error("Config file was not readable!", "\n", e)
    return False
  except yaml.parser.ParserError as e:
    error("Config file was not parsable!", "\n", e)
    return False

def loadProtocols():
  global protocols
  for p in data["protocols"] or []:
    try:
      if protocols.get(p, None) == None:
        protocols[p] = __import__("protocols." + p)
        protocols[p] = getattr(protocols[p], p)
      else:
        mreload(protocols[p])
      ok("Loaded protocol:", p)
    except ModuleNotFoundError:
      error("Could not find protocol:", p)

def loadFilter():
  global filters
  for p in data["filter"] or []:
    try:
      if filters.get(p, None) == None:
        filters[p] = __import__("filter." + p)
        filters[p] = getattr(filters[p], p)
        filters[p].enabled = True
      else:
        mreload(filters[p])
      ok("Loaded filter:", p)
    except ModuleNotFoundError:
      error("Could not find filter:", p)

def disableFilter(name):
  filters[name].enabled = False

def enableFilter(name):
  filters[name].enabled = True

def loadActions():
  global actions
  for p in data["actions"] or []:
    try:
      if actions.get(p, None) == None:
        actions[p] = __import__("actions." + p)
        actions[p] = getattr(actions[p], p)
      else:
        mreload(actions[p])
      ok("Loaded action:", p)
    except ModuleNotFoundError:
      error("Could not find action:", p)

def checkInterfaces():
  ok("Network-interfaces are", data["interface1"], "&", data["interface2"])