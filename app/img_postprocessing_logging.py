from time import sleep
from PIL import Image
from send2trash import send2trash
from exif_or_encodedate_from_filename import add_exifdate_to_img, add_exifdate_newmethod
import os, sys, subprocess
from raw import convert2raw
from unlimited_ai_img import now, write_to_output
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



def img_postprocessing_logging(
        old_filepath_url:str, 
        savedir: str, 
        new_filename_no_ext:str,
        if_method_is_hftoken:bool=False
        ):
  
  # convert image to jpg
  for i in range(3):
    try:
      if if_method_is_hftoken == False:  os.path.exists(old_filepath_url) # if uses file download method, no direct data stream
      image = Image.open(old_filepath_url)
      image = image.convert('RGB')
      if not os.path.exists(savedir):  os.makedirs(savedir)
      image.save(f"{savedir}{slash}{new_filename_no_ext}.jpg")
      write_to_output('img_new_filepath', f"{savedir}{slash}{new_filename_no_ext}.jpg")
      break
    except OSError:
      if i < 3:
        print(MAGENTA+"Image download not completed yet. Retrying..."+RESET, end="\r")
        sleep(5)
      else:   raise Exception("Image failed to process. Return to base.")
      
  # send2trash old webp image
  # cannot remove folder!!! imagine send2trash downloads folder (duh) 
  if if_method_is_hftoken == False:  send2trash( old_filepath_url )

  # add exif date to image based on, not include working directory
  add_exifdate_newmethod(f"{savedir}{slash}{new_filename_no_ext}.jpg")



def main():
  import tomli
  from rename_to_current_time import return_renamed
  from time import sleep
  from filesIngest import filesIngest

  rr = filesIngest()
  rr.select_files('images') ## IMAGES or VIDEOS valid
  
  ### load toml config file
  with open("config_dev.toml", "rb") as f:
    data = tomli.load(f)

  ## assign toml parsed data as variable
  savepath:str     = data['file_management']['savedir']
  opendir_bool:bool= data['file_management']['open_folder_after_execution']
  
  for file in rr.getFileList():
    # giving a name
    newfn_noext: str = return_renamed()
    img_postprocessing_logging(
      file,
      savepath,
      newfn_noext
      )
    sleep(1)
  
  # invoke opening folder if true
  if opendir_bool:   open_folder(savepath)



# run this code if runned directly,
# this will not run if this script is imported as module
if __name__ == "__main__":  main()