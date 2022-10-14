import sys,os
from datetime import datetime,timedelta
from dotenv import load_dotenv
load_dotenv()

ENCODING = 'UTF-8'
IS_WIN32 = False
IS_LINUX = False

if sys.platform == 'win32':
  IS_WIN32 = True
elif sys.platform == 'linux':
  IS_LINUX = True

ARGV = {}

# 0:NONE 1:ERROR 2:WARNING 3:INFO 4:DEBUG
VerboseLevel = 3
VerboseLevel = 4 if os.getenv('VERBOSE') or ('-v' in sys.argv or '--verbose' in sys.argv) else VerboseLevel

SERVER_TICK_INTERVAL = 60

def format_curtime():
  return datetime.strftime(datetime.now(), '%H:%M:%S')

def log_error(*args, **kwargs):
  if VerboseLevel >= 1:
    print(f"[{format_curtime()}] [ERROR]:", *args, **kwargs)

def log_warning(*args, **kwargs):
  if VerboseLevel >= 2:
    print(f"[{format_curtime()}] [WARNING]:", *args, **kwargs)

def log_info(*args, **kwargs):
  if VerboseLevel >= 3:
    print(f"[{format_curtime()}] [INFO]:", *args, **kwargs)

def log_debug(*args, **kwargs):
  if VerboseLevel >= 4:
    print(f"[{format_curtime()}] [DEBUG]:", *args, **kwargs)
