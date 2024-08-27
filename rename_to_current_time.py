import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from datetime import datetime

def return_renamed():
  
  # while True:
    
    # try:
      
  now = datetime.now()
  now_str: str = now.strftime('FLUX_%Y%m%d_%H%M%S')
  return now_str
      
      # os.rename(oldfilename, now_str)
      # print(Fore.GREEN + 'Renaming '+ oldfilename + ' to new filename ' + newfilename + ' completed successfully.' + Style.RESET_ALL)
      # break
    
    # except FileExistsError:
    #   print(Fore.LIGHTMAGENTA_EX + 'File '+ newfilename + ' already exists.' + Style.RESET_ALL, end=' ')
    #   newfilename = fixFileExists(newfilename)
    #   print(Fore.LIGHTMAGENTA_EX + 'Increment by 1 to ' + newfilename)
