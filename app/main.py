import base64
import json
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Style

from hf_api import hf_api_fastapi
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
  
  data = hf_api_fastapi(prompt)
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
      "Access-Control-Allow-Origin": "https://imagen.ai.iziizz.com"
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
      "Access-Control-Allow-Origin": "https://imagen.ai.iziizz.com"
    }, 
    media_type="application/json", 
  )
  # maknanya logic utk nk display gambar 1 ke, 2 ke, 3 ke, dsbgnya, logic tu nanti implement dkt javascript.
  # memang functionality utk api JUST for fetch data. Any logic implement di client side.


# pls follow tutorial from https://medium.com/@m.adel.abdelhady/deploying-fastapi-app-over-https-with-traefik-a-quick-step-by-step-guide-d440e87d8f44 to deploy with HTTPS


# cd app; uvicorn main:app --reload 
# (run this many times until no error emerges, 



# pip freeze > requirements.txt
# pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client
# (if you are on windows) pip install pywin32