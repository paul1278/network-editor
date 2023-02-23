import yaml
from yaml.loader import SafeLoader
from utils import *

data = None
protocols = {}
filters = {}
actions = {}

def load():
  global data
  try:
    # Open the file and load the file
    with open('./config.yaml') as f:
      data = yaml.load(f, Loader=SafeLoader)
      loadProtocols()
      loadActions()
      loadFilter()
      checkInterfaces()
      data["debug"] = data.get("debug", False)
      setDebug(data["debug"])
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
      protocols[p] = __import__("protocols." + p)
      protocols[p] = getattr(protocols[p], p)
      ok("Loaded protocol:", p)
    except ModuleNotFoundError:
      error("Could not find protocol:", p)

def loadFilter():
  global filters
  for p in data["filter"] or []:
    try:
      filters[p] = __import__("filter." + p)
      filters[p] = getattr(filters[p], p)
      ok("Loaded filter:", p)
    except ModuleNotFoundError:
      error("Could not find filter:", p)

def loadActions():
  global actions
  for p in data["actions"] or []:
    try:
      actions[p] = __import__("actions." + p)
      actions[p] = getattr(actions[p], p)
      ok("Loaded action:", p)
    except ModuleNotFoundError:
      error("Could not find action:", p)

def checkInterfaces():
  ok("Network-interfaces are", data["interface1"], "&", data["interface2"])