FROM tiangolo/uvicorn-gunicorn:python3.9

COPY ./nolimit-genai-img /app/

RUN curl -L https://exiftool.org/Image-ExifTool-12.96.tar.gz | tar -zxvf
RUN mv Image-ExifTool-12.96 /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client