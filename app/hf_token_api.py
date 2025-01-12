from base64 import b64encode
import io
import requests
from random import randint
from img_postprocessing_logging import img_pp
from toml_ingest import config_data
cf = config_data()
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX


def main(prompt:str):
  # show what hf token picked
  hftoken_lucky = randint(0, len(cf['tokens'])-1)
  print(MAGENTA, "HF_Token:", cf['tokens'][hftoken_lucky], RESET)

  # Make the API request
  response = requests.post(
    f"https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
    headers={"Authorization": f"Bearer {cf['tokens'][hftoken_lucky]}"},
    json = {
    "inputs": prompt,
    "parameters": {
      "width": 768,
      "height": 1024, # portrait
      "seed": randint(0, 2_147_483_647)
    },
    "options": {
      "inference_count": 18
    }
    }
  )
  image_base64 = b64encode(response.content).decode('utf-8')
  img_pp(
    io.BytesIO(response.content),
    if_method_is_hftoken=True
  )
  return image_base64


if __name__ == "__main__":
  prompt = input("Input prompt: ")
  main(prompt)