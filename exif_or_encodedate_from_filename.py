import subprocess
import os
from datetime import datetime
from time import sleep
import platform
import sys
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style

if platform.system() == 'Windows':
  import win32file
  import pywintypes


slash = "\\" if sys.platform == "win32" else "/"

exiftool_location = r"C:\Program Files\XnViewMP\AddOn" # "/root/Image-ExifTool-12.96"
mediatype = 'images' ### IMAGES / VIDEOS



def getImageDate(filepath):
  date_str = os.path.splitext(os.path.basename(filepath))[0].split("_")[1]
  time_str = os.path.splitext(os.path.basename(filepath))[0].split("_")[2]
  date_obj = datetime.strptime(date_str, "%Y%m%d")  ## this must be true otherwise ERR
  
  try:
    time_obj = datetime.strptime(time_str, "%H%M%S")
  
  except:
    print(Fore.MAGENTA + 'Error parsing time string '+ time_str+ ', possibly invalid character. Replacing with 00:00:00' + Style.RESET_ALL)
    time_str = '000000'
    time_obj = datetime.strptime(time_str, "%H%M%S")
  
  datetime_obj = datetime.combine(date_obj.date(), time_obj.time())
  return datetime_obj




#############
### MAINN ###
#############



print(Style.RESET_ALL)


def add_exifdate_to_img(filename):
  
  try:
    
    datetime_obj = getImageDate(filename)

    ## change EXIF trio dates
    command = [f'{exiftool_location}{slash}exiftool', 
               f'-AllDates="{datetime_obj}"',
               f'-overwrite_original',
               f'"{filename}"']
    ### YES WINDOWS TERMINAL CAN ONLY INTERPRET DOUBLE QUOTE AS ENCLOSING FOR ANY ARGUMENT PASS THAT HAS SPACES!
    print(command)
    subprocess.run(command)
    


    ## change THE file creation date and modified date
    
    timestamp = datetime_obj.timestamp()
    if platform.system() == 'Windows':
      # Convert timestamp to Windows file time
      wintime = pywintypes.Time(timestamp)
      winfile = win32file.CreateFile(
        filename, win32file.GENERIC_WRITE, win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, 0, 0
      )
      win32file.SetFileTime(winfile, wintime, wintime, wintime)
      winfile.close()
    else:
      # Set access and modification times (creation time not modifiable on Unix-like systems)
      os.utime(filename, (timestamp, timestamp))
    
    
    ## print success statement
    print(Fore.GREEN + os.path.basename(filename) + ' EXIF data has been changed to ' + datetime_obj.strftime("%d/%m/%Y %H:%M:%S"))
    print(Style.RESET_ALL)
    sleep(0.2)



  except Exception:
    print(Fore.RED + 'An error has occured. Please check the exception below for error.')
    print(Fore.RED + str(Exception))
    print(Style.RESET_ALL)
    exit(1)


