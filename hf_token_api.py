import requests
from random import randint


def hf_token(hf_token:str, model:str, prompt:str, width:int, height:int, inference_count:int):
  # Construct the payload with dynamic parameters for width, height, and inference count
  """
  Make an API request to the Hugging Face inference API using the given
  parameters.

  Parameters
  ----------
  hf_token : str
    The token to use for authentication.
  model : str
    The model to use for the request.
  prompt : str
    The prompt to use for the request.
  width : int
    The width of the output image.
  height : int
    The height of the output image.
  inference_count : int
    The number of times to run the model with the given prompt.

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
  payload = {
    "inputs": prompt,
    "parameters": {
      "width": width,
      "height": height,
      "seed": randint(1000000, 9999999)
    },
    "options": {
      "inference_count": inference_count
    }
  }
  
  # Make the API request
  response = requests.post(
    f"https://api-inference.huggingface.co/models/{model}", 
    headers={"Authorization": f"Bearer {hf_token}"}, 
    json=payload
  )
  
  return response.content
