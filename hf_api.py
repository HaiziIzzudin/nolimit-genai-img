from rename_to_current_time import return_renamed
from change_proxy import getNewIP
from img_postprocessing_logging import img_postprocessing_logging, open_folder
from unlimited_ai_img import config_data, write_to_output, now
cf = config_data()
from hf_token_api import hf_token

# from test import full_prompt
from gradio_client import Client
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX
import io





def newIP_and_load_hf_model(hf_model:str):
  while True:
    try:
      getNewIP('api')  # 'api' | 'selenium'
      write_to_output('hf_model', hf_model)
      write_to_output('model_load_begin', now())
      print(Fore.YELLOW, f"\nLoading HF {hf_model} model...",Fore.GREEN)
      client = Client(hf_model, ssl_verify=False)
      print(Style.RESET_ALL)
      write_to_output('model_load_end', now())
      write_to_output('model_load_status', 'success')
      return client
    except Exception as e:
      write_to_output('model_load_end', now())
      write_to_output('model_load_status', 'failed')
      write_to_output('model_load_failed_reason', str(e), True)
      print(Fore.LIGHTRED_EX, f"\nLoading {hf_model} model failed. Error can be checked from 'output.log'.\nChanging proxy...", Style.RESET_ALL)



def run_inference(client, loop_number:int, inference_steps:int):
  print(Fore.LIGHTMAGENTA_EX, f"Run #{loop_number}.\nFree compute yields longer results. Please be patient...", Style.RESET_ALL)
  try:
    write_to_output('prompt', cf['prompt'])
    write_to_output('randomized_seed', True)
    write_to_output('img_output_width', cf['width'])
    write_to_output('img_output_height', cf['height'])
    write_to_output('guidance_scale', 3.5)
    write_to_output('inference_steps', inference_steps)
    write_to_output('api_name', '/infer')
    write_to_output('model_inference_begin', now())
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
    write_to_output('model_inference_end', now())
    write_to_output('model_inference_status', 'success')
    image_path:str = result[0]
    write_to_output('img_old_filepath', image_path)
    return {
      "generation bool": True,
      "path/message": image_path
      }
  except Exception as e:
    write_to_output('model_inference_end', now())
    write_to_output('model_inference_status', 'failed')
    write_to_output('model_inference_failed_reason', str(e), True)
    return {
      "generation bool": False,
      "path/message": Fore.LIGHTRED_EX+f"\nClient disconnected. Error can be checked from 'output.log'.\nReconnecting you to other proxy server...\n"+Style.RESET_ALL
      }


class master():
  def run(self, model_name:str, prompt:str, width:int, height:int, inference_count:int):
    """
    Runner function for generating images using HuggingFace's API.

    Parameters:
        model_name (str): Model name to use for image generation.
        prompt (str): Prompt for image generation.
        width (int): Width of the output image.
        height (int): Height of the output image.
        inference_count (int): Number of times to run the model with the given prompt.

    Returns:
        None
    """
    try:
      token_list = cf['tokens']
      for j in range(len(token_list)):
        try:
          content = hf_token(
            token_list[j],
            model_name,
            prompt,
            width, height,
            inference_count
          )
          break
        except:
          print(YELLOW,f'Token #{j+1} exhausted. Using next token...',RESET)
      self.newname = return_renamed()
      img_postprocessing_logging(
        io.BytesIO(content),
        cf['savepath'],
        self.newname, True
      )
    
    except:
      print(YELLOW,f'Exhausted all user tokens. Fallback to anonymous user...',RESET)
      client = newIP_and_load_hf_model(cf['model_name'])
      imgpath = run_inference(client, i+1, cf['inference_count'])

      while not imgpath['generation bool']: # gen bool => false => not => true
        print(imgpath['path/message'])  ## MESSAGE: changing server
        client = newIP_and_load_hf_model(cf['model_name'])
        imgpath = run_inference(client, i+1, cf['inference_count'])
      else: # gen bool => true => not => false
        self.newname = return_renamed()
        img_postprocessing_logging(
          imgpath['path/message'], 
          cf['savepath'], 
          self.newname
        )
  
  def return_for_api(self):
    with open(f"{cf['savepath']}/{self.newname}.jpg", 'rb') as f:   return f.read()
  def return_for_local(self):
    return







########################
### FINAL STAGE HERE ###
########################


mtr = master()

def hf_api_fastapi(prompt):
  print(MAGENTA,f'FASTAPI: Generating image...',RESET)
  mtr.run(
    'black-forest-labs/FLUX.1-dev',
    prompt,
    768, 1024, 20
  )
  return mtr.return_for_api() # this return image binary

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