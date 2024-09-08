import tomli as tomllib
import json
from datetime import datetime
from os.path import exists
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX


new_dict = {}
new_dict['timestamp_begin'] = datetime.now().isoformat()
def write_to_output(key:str, value, ending:bool=False):
  if ending == False:
    new_dict[key] = value
  elif ending == True:
    new_dict[key] = value
    new_dict['timestamp_end'] = datetime.now().isoformat()
    json_obj = json.dumps(new_dict, indent=2)
    with open("output.log", "a") as f:
      f.write(json_obj)
      f.write(',\n')

def now():
  return datetime.now().isoformat()




def config_data():
  """
  This function configures and returns data from a TOML configuration file.
  
  It extracts various parameters such as 'profile_path', 'model name', 'inference', 
  'prompt', 'gen_count', 'width', 'height', 'savepath', 'opendir_on_finish', 
  and 'proxy_finder_ver'.
  
  Returns:
    A dictionary containing the extracted configuration data with the following keys:
      'profile_path' list[str] 
      'tokens' list[str]
      'model_name' (str)
      'inference_count' (int) 
      'prompt' (str)
      'gen_count' (int) 
      'width' (int)
      'height' (int)
      'savepath' (str)
      'opendir_on_finish' (bool)
      'proxy_finder_ver' (int) 
  """
  try:
    ### assign toml parsed data as variable
    width_height:str = data['generation']['image_dimension'].split('x')

    return {
      'profiles': data['profile']['profile'],  # this one return array of an array of boolean, and firefox profile path
      'tokens': data['token']['token'], # return array of hf token
      'model_name': data['model']['model_name'],
      'inference_count': data['model']['inference'],
      'prompt': data['generation']['prompt'],
      'gen_count': data['generation']['generation_count'],
      'width': int(width_height[0]),
      'height': int(width_height[1]),
      'savepath': data['file_management']['savedir'],
      'opendir_on_finish': data['file_management']['open_folder_after_execution'],
      'proxy_finder_ver': data['developer']['proxy_finding_version']
    }
  except KeyError as e:
    print(RED,e,'Please make sure all variable inside config file is comply with the guideline given.',RESET)


### load toml config file once, then use the data indefinitely
### add _dev for dev
config_dev = "config_dev.toml"
if not exists(config_dev):
  config_file = "config.toml"
else:
  print(MAGENTA,"DEV CONFIG FILE FOUND. YOU ARE NOW A DEVELOPER.",RESET)
  config_file = config_dev


with open(config_file, "rb") as f:
  data = tomllib.load(f)



if __name__ == '__main__':
  conf = config_data()
  # print(conf['profile_path'])

  write_to_output('hello', 'how are you')
  write_to_output('bye', 'see you soon', True)