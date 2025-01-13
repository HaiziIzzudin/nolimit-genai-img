from uuid import uuid4 as uuid
from time import sleep
from PIL import Image
from send2trash import send2trash
import os, sys, subprocess
from colorama import Fore, Style
from datetime import datetime
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX


def open_folder(filename):
  if sys.platform == "win32":
    os.startfile(filename)
  else:
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filename])


slash = "\\" if sys.platform == "win32" else "/"
pwd = os.getcwd()


def img_pp(old_filepath_url:str, method_is_hftoken:bool=False):
  
  # convert image to jpg
  if method_is_hftoken == False:  sleep(3) # if uses file download method, no direct data stream
  image = Image.open(old_filepath_url)
  image = image.convert('RGB')

  # newname_noext = uuid() # assign a random name
  newname_noext = datetime.now().strftime("FLUX_%Y%m%d_%H%M%S_%f") # assign a random name

  
  if "TERMUX_VERSION" in os.environ:
    output_folder = f"{os.path.expanduser('~')+ slash + 'storage' + slash + 'downloads' + slash}output"
  elif (sys.platform == "win32") or (sys.platform == "linux"):
    output_folder = f"{pwd + slash}output"
  
  os.mkdir(output_folder) if not os.path.exists(output_folder) else None
  image.save(f"{output_folder+slash}{newname_noext}.jpg")
      
  # send2trash old webp image
  # cannot remove folder!!! imagine send2trash downloads folder (duh) 
  if method_is_hftoken == False:  send2trash( old_filepath_url )
