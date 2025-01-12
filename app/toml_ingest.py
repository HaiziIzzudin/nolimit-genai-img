import sys
import tomli as tomllib
from datetime import datetime
from os.path import exists
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX


new_dict = {}
new_dict['timestamp_begin'] = datetime.now().isoformat()


def config_data():
  """
  This function configures and returns data from a TOML configuration file.
  
  Returns:
    A dictionary containing the extracted configuration data with the following keys:
      'profile_path' list[str] 
      'tokens' list[str]
      'opendir_on_finish' (bool)
  """

  return {
    'profiles': data['profile']['profile'],  # this one return array of an array of boolean, and firefox profile path
    'profiles_only': [i[1] for i in data['profile']['profile'] if i[0]],  # return list of only path to profile
    'tokens': data['token']['token'], # return array of hf token
  }


### load toml config file once, then use the data indefinitely
### add _dev for dev

if sys.platform == "win32":       # why no trailing folder?
  config_dev = "config_dev.toml"  # bcos tests with uvicorn, need to cd to app folder first 
  config_file = "config.toml"     # (make sure config / config_dev file in app folder)
else:
  config_dev = "config_dev.toml"
  config_file = "/code/app/config.toml"

if exists(config_dev): 
  print(MAGENTA,"DEV CONFIG FILE FOUND. YOU ARE NOW A DEVELOPER.",RESET)
  config_file = config_dev


with open(config_file, "rb") as f:
  data = tomllib.load(f)



if __name__ == '__main__':
  conf = config_data()
  # print(conf['profile_path'])