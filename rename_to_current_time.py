import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from datetime import datetime

def return_renamed():
  """
  Return a string representing the current datetime, in the format:
  `FLUX_<year><month><day>_<hour><minute><second>`

  This string is used as a filename for the generated image.
  """

  now = datetime.now()
  now_str: str = now.strftime('FLUX_%Y%m%d_%H%M%S')
  return now_str