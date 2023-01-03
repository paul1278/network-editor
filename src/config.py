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
  except FileNotFoundError:
    error("Config file was not found!")

def loadProtocols():
  global data, protocols
  for p in data["protocols"] or []:
    try:
      protocols[p] = __import__("protocols." + p)
      ok("Loaded protocol:", p)
    except ModuleNotFoundError:
      error("Could not find protocol:", p)

def loadFilter():
  global data, filters
  for p in data["filter"] or []:
    try:
      filters[p] = __import__("filter." + p)
      ok("Loaded filter:", p)
    except ModuleNotFoundError:
      error("Could not find filter:", p)

def loadActions():
  global data, actions
  for p in data["actions"] or []:
    try:
      actions[p] = __import__("actions." + p)
      ok("Loaded action:", p)
    except ModuleNotFoundError:
      error("Could not find action:", p)