import yaml
from yaml.loader import SafeLoader
from utils import *

data = None

def load():
  global data
  try:
    # Open the file and load the file
    with open('./config.yaml') as f:
      data = yaml.load(f, Loader=SafeLoader)
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
