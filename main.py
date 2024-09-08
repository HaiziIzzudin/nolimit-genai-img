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
    returned_data = hf_api_fastapi(prompt)
    filename = returned_data['filename']
    image_binary = returned_data['data']
    return Response(
        content=f"{base64.b64encode(image_binary).decode('utf-8')}", 
        media_type="text/html", 
        headers={"Content-Disposition": f"{filename}"}
    )


# uvicorn main:app --reload (run this many times until no error emerges, 
# make new directory named output in the same folder as git cloned,
# change exiftool directory to reflect linux (dont forget download Exiftool),
# then run fastapi run main.py)
# pip freeze > requirements.txt
# pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client
# please comment out line 83 of file img_postprocessing_logging.py to avoid errors