from random import randint
from toml_ingest import config_data
cf = config_data()
from gradio_client import Client
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from PIL import Image
from send2trash import send2trash
from datetime import datetime
import os
import sys
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX



def main(prompt:str):
  # get hf_token
  hftoken_index = randint(0, len(cf['tokens'])-1)
  token = cf['tokens'][hftoken_index]
  print(MAGENTA, "HF_Token:", token, RESET)

  # main command
  # client = Client(src="black-forest-labs/FLUX.1-dev", ssl_verify=False, hf_token=token)
  # result = client.predict(
  #   prompt=prompt,
  #   seed=0,
  #   randomize_seed=True,
  #   width=768,
  #   height=1024,
  #   guidance_scale=3.5,
  #   num_inference_steps=18,
  #   api_name="/infer"
  # )

  client = Client("DamarJati/FLUX.1-RealismLora", ssl_verify=False, hf_token=token)
  result = client.predict(
    prompt=prompt,
    steps=20,
    randomize_seed=True,
    width=768,
    height=1024,
    api_name="/run_lora"
  )
  
  print(result)

  # Load the image from the result path
  image_path = result[0]
  print(MAGENTA, "Image path: ", image_path, RESET)
  image = Image.open(image_path)

  # Convert the image to JPG and save to a new location
  new_image_path = "output/" + datetime.now().strftime("FLUX_%Y%m%d_%H%M%S_%f") + ".jpg"
  
  # Create the output folder if it doesn't exist
  pwd = os.getcwd()
  slash = "\\" if sys.platform == "win32" else "/"
  os.mkdir(f"{pwd+slash}output") if not os.path.exists(f"{pwd+slash}output") else None
  
  image.convert("RGB").save(new_image_path, "JPEG")
  print(GREEN, "Image saved as:", new_image_path, RESET)

  # Delete the image from the result path
  send2trash(image_path)





if __name__ == "__main__":
  prompt = input("Input prompt: ")
  main(prompt)