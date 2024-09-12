from uuid import uuid4 as uuid
from time import sleep
from PIL import Image
from send2trash import send2trash
from exif_or_encodedate_from_filename import add_exifdate_to_img, add_exifdate_newmethod
import os, sys, subprocess
from colorama import Fore, Style
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


def img_pp(
        old_filepath_url:str, 
        if_method_is_hftoken:bool=False
        ):
  
  # convert image to jpg
  if if_method_is_hftoken == False:  sleep(3) # if uses file download method, no direct data stream
  image = Image.open(old_filepath_url)
  image = image.convert('RGB')
  newname_noext = uuid() # assign a random name
  image.save(f"{pwd+slash}output{slash}{newname_noext}.jpg")
      
  # send2trash old webp image
  # cannot remove folder!!! imagine send2trash downloads folder (duh) 
  if if_method_is_hftoken == False:  send2trash( old_filepath_url )

  if sys.platform == "win32":
    # add exif date to image based on, not include working directory
    add_exifdate_newmethod(f"{pwd+slash}output{slash}{newname_noext}.jpg")







def main():
  import tomli
  from time import sleep
  from filesIngest import filesIngest

  rr = filesIngest()
  rr.select_files('images') ## IMAGES or VIDEOS valid
  
  for file in rr.getFileList():
    # giving a name
    img_pp(
      file,
      )
    sleep(1)
  
  # invoke opening folder if true
  open_folder(f"{pwd+slash}output")



# run this code if runned directly,
# this will not run if this script is imported as module
if __name__ == "__main__":  main()