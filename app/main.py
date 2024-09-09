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

@app.post("/generate")
async def generate(prompt_request: PromptRequest):
    prompt = prompt_request.prompt
    print(MAGENTA,prompt,RESET)
    returned_data = hf_api_fastapi(prompt)
    image_binary = returned_data['data']
    return Response(
        content=f"{base64.b64encode(image_binary).decode('utf-8')}", 
        media_type="text/html", 
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
      media_type="application/json", 
    )
    # maknanya logic utk nk display gambar 1 ke, 2 ke, 3 ke, dsbgnya, logic tu nanti implement dkt javascript.
    # memang functionality utk api JUST for fetch data. Any logic implement di client side.


# pls follow tutorial from https://medium.com/@m.adel.abdelhady/deploying-fastapi-app-over-https-with-traefik-a-quick-step-by-step-guide-d440e87d8f44 to deploy with HTTPS
# before run docker compose up -d, add HF token to config.toml file, and
# cp nolimit-genai-img/Dockerfile ./


# cd app; uvicorn main:app --reload (run this many times until no error emerges, 
# make new directory named output in the same folder as git cloned,
# change exiftool directory to reflect linux (dont forget download Exiftool),
# then run fastapi run main.py)
# pip freeze > requirements.txt
# pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client
# (if you are on windows) pip install pywin32
# please comment out line 83 of file img_postprocessing_logging.py to avoid errors