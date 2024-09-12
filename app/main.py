import asyncio
import base64
import json
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Style

from hf_token_api import hf_token_api
from imagefx_selenium import return_for_api as imagefx_api
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX


    
app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # Allows all origins
  allow_credentials=True,
  allow_methods=["*"],  # Allows all methods
  allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
  return {"What is this?": "Haizukun's Image Gen API using FASTAPI"}


class PromptRequest(BaseModel): # this is for json body
  prompt: str

@app.post("/flux-generate")
async def generate(prompt_request: PromptRequest):
  
  prompt = prompt_request.prompt
  print(MAGENTA,"Prompt:",prompt,RESET)
  
  # data = hf_api_fastapi(prompt)

  while True: 
    try:
      task1 = asyncio.to_thread(hf_token_api, prompt, 0)
      break
    except Exception as e:
      print(f"Error: {e}. Retrying...")
  # task2 = asyncio.to_thread(hf_token_api, prompt, 1)
  
  data1 = await asyncio.gather(task1) # return base64 data

  image_base64:list[str] = [data1]
  
  total = len(image_base64)

  print(MAGENTA,"total:",total,RESET)

  return Response(
    content=json.dumps(
      {
        "image_base64": image_base64,  # you already returned base64 list
        "total": total
      }), 
    headers={
      "Access-Control-Allow-Origin": "https://imagen.ai.iziizz.com",
      "Access-Control-Allow-Methods": "POST",
      "Access-Control-Allow-Headers": "Content-Type",
    }, 
    media_type="application/json", 
  )


@app.post("/imagefx-generate")
async def generate(prompt_request:PromptRequest):
    
  prompt = prompt_request.prompt
  print(MAGENTA,"Prompt:",prompt,RESET)
  
  data = imagefx_api(prompt)
  image_base64:list[str] = data[0]
  total = data[1]
  print(MAGENTA,"total:",data[1],RESET)
  
  return Response(
    content=json.dumps(
      {
        "image_base64": image_base64,  # you already returned base64 
        "total": total
      }), 
    headers={
      "Access-Control-Allow-Origin": "https://imagen.ai.iziizz.com",
      "Access-Control-Allow-Methods": "POST",
      "Access-Control-Allow-Headers": "Content-Type",
    }, 
    media_type="application/json", 
  )
  # maknanya logic utk nk display gambar 1 ke, 2 ke, 3 ke, dsbgnya, logic tu nanti implement dkt javascript.
  # memang functionality utk api JUST for fetch data. Any logic implement di client side.




# uvicorn main:app --reload 
# (run this many times until no error emerges, 



# pip freeze > requirements.txt
# pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client
# (if you are on windows) pip install pywin32