from base64 import b64encode
import io
from uuid import uuid4 as uuid
import requests
from random import randint
from img_postprocessing_logging import img_pp
from unlimited_ai_img import config_data
cf = config_data()
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX


def hf_token_api(prompt:str, hftoken_index:int):
  # Construct the payload with dynamic parameters for width, height, and inference count
  """
  Make an API request to the Hugging Face inference API using the given
  parameters.

  Parameters
  ----------
  hf_token : str
    The token to use for authentication.
  prompt : str
    The prompt to use for the request.

  Returns
  -------
  response.content : bytes
    The response content from the API request, please use code snippet:
    ```
    image = Image.open(io.BytesIO(use_token(...)))\n
    image = image.convert('RGB')\n
    image.save(f"test1.jpg")
    ```
    to interpret and save the photo.
  """
  # show what hf token picked
  print("HF_Token:", cf['tokens'][hftoken_index])

  # Make the API request
  response = requests.post(
    f"https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
    headers={"Authorization": f"Bearer {cf['tokens'][hftoken_index]}"},
    json = {
    "inputs": prompt,
    "parameters": {
        "width": 768,
        "height": 1024,
        "seed": randint(100_000_000, 999_999_999)
    },
    "options": {
        "inference_count": 18
    }
    }
  )
  newname = uuid()
  print(MAGENTA,"newname:",newname,RESET)
  img_pp(
    io.BytesIO(response.content),
    True
  )
  image_base64 = b64encode(response.content).decode('utf-8')
  return image_base64
