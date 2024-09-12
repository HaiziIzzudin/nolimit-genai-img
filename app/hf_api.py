from change_proxy import getNewIP
from img_postprocessing_logging import img_pp, open_folder
from unlimited_ai_img import config_data
cf = config_data()

# from test import full_prompt
from gradio_client import Client
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX





def newIP_and_load_hf_model(hf_model:str):
  while True:
    try:
      getNewIP('api')  # 'api' | 'selenium'
      print(Fore.YELLOW, f"\nLoading HF {hf_model} model...",Fore.GREEN)
      client = Client(hf_model, ssl_verify=False)
      print(Style.RESET_ALL)
      return client
    except Exception as e:
      print(Fore.LIGHTRED_EX, f"\nLoading {hf_model} model failed. Error can be checked from 'output.log'.\nChanging proxy...", Style.RESET_ALL)



def run_inference(client, loop_number:int, inference_steps:int):
  print(Fore.LIGHTMAGENTA_EX, f"Run #{loop_number}.\nFree compute yields longer results. Please be patient...", Style.RESET_ALL)
  try:
    result = client.predict(
      prompt=cf['prompt'],
      seed=0,
      randomize_seed=True,
      width=cf['width'],
      height=cf['height'],
      guidance_scale=3.5,
      num_inference_steps=inference_steps,
      api_name="/infer"
    )
    image_path:str = result[0]
    return {
      "generation bool": True,
      "path/message": image_path
      }
  except Exception as e:
    return {
      "generation bool": False,
      "path/message": Fore.LIGHTRED_EX+f"\nClient disconnected. Error can be checked from 'output.log'.\nReconnecting you to other proxy server...\n"+Style.RESET_ALL
      }


class master():
  def run(self):
    
    client = newIP_and_load_hf_model(cf['model_name'])
    imgpath = run_inference(client, i+1, cf['inference_count'])

    while not imgpath['generation bool']: # gen bool => false => not => true
      print(imgpath['path/message'])  ## MESSAGE: changing server
      client = newIP_and_load_hf_model(cf['model_name'])
      imgpath = run_inference(client, i+1, cf['inference_count'])
    else: # gen bool => true => not => false
      img_pp(
        imgpath['path/message'], 
      )
  
  def return_for_local(self):
    return







########################
### FINAL STAGE HERE ###
########################


mtr = master()

if __name__ == '__main__':
  print(f"Proxy finding version: {cf['proxy_finder_ver']}\n")
  print('Prompt:\n', cf['prompt'])
  for i in range(cf['gen_count']):
    print(MAGENTA,f'LOCAL: Generating image #{i+1}...',RESET)
    mtr.run(
      cf['model_name'],
      cf['prompt'],
      cf['width'], cf['height'],
      cf['inference_count'],
    )
  # invoke opening folder if true
  if cf['opendir_on_finish']:   open_folder(cf['savepath'])