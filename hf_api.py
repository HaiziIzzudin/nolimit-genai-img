from rename_to_current_time import return_renamed
from change_proxy import getNewIP
from img_postprocessing_logging import img_postprocessing_logging, open_folder
from unlimited_ai_img import config_data, write_to_output, now
cf = config_data()

# from test import full_prompt
from gradio_client import Client
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style





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
  print(Fore.LIGHTMAGENTA_EX, f"\nRun #{loop_number}.\nFree compute yields longer results. Please be patient...", Style.RESET_ALL)
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











############
### MAIN ###
############

print(f"Proxy finding version: {cf['proxy_finder_ver']}\n")

print('Prompt:\n', cf['prompt'])

client = newIP_and_load_hf_model(cf['model_name'])

i = 0
while i < cf['gen_count']:
  imgpath = run_inference(client, i+1, cf['inference_count'])

  if imgpath['generation bool'] == False:
    print(imgpath['path/message'])  ## NOTICE: changing server
    client = newIP_and_load_hf_model(cf['model_name'])
    # no increment here bcos it still failed to 
    # generate current photo index, therefore loop again
  
  else:
    # giving a name
    newfn_noext: str = return_renamed()
    # postprocess photo
    img_postprocessing_logging(imgpath['path/message'], cf['savepath'], newfn_noext)
    i += 1


# invoke opening folder if true
if cf['opendir_on_finish']:   open_folder(cf['savepath'])