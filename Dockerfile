FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client

COPY ./app /code/app

RUN mkdir /code/app/output

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]