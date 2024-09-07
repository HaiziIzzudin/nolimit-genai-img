import base64
from pydantic import BaseModel
from hf_api import hf_api_fastapi
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Style
from tomli import load
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX

app = FastAPI()

with open("config_dev.toml", "rb") as f:
    data = load(f)
    print(data['developer']['cors_allow_origin_url'])


app.add_middleware(
    CORSMiddleware,
    allow_origins=data['developer']['cors_allow_origin_url'],  # Allows all origins
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
    image_binary = hf_api_fastapi(prompt)
    return Response(content=f"{base64.b64encode(image_binary).decode('utf-8')}", media_type="text/html")


# uvicorn main:app --reload
# pip freeze > requirements.txt
# pip install colorama pysocks requests free-proxy tomli pillow send2trash pywin32