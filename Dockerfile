FROM tiangolo/uvicorn-gunicorn:python3.9

COPY ./nolimit-genai-img /app/

RUN wget https://exiftool.org/Image-ExifTool-12.96.tar.gz
RUN tar -zxvf Image-ExifTool-12.96.tar.gz

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client