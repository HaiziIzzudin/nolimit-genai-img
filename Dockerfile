FROM python:3.9

RUN apt-get update -y \
  && apt-get install --no-install-recommends --no-install-suggests -y tzdata ca-certificates bzip2 curl wget libc-dev libxt6 \
  && apt-get install --no-install-recommends --no-install-suggests -y `apt-cache depends firefox-esr | awk '/Depends:/{print$2}'` \
  && update-ca-certificates \
  # Cleanup unnecessary stuff
  && apt-get purge -y --auto-remove \
                -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* /tmp/*

# install geckodriver

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz && \
    tar -zxf geckodriver-v0.35.0-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v0.35.0-linux64.tar.gz

# install firefox

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    wget -O $FIREFOX_SETUP "https://download-installer.cdn.mozilla.net/pub/firefox/releases/130.0/linux-x86_64/en-US/firefox-130.0.tar.bz2" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install "fastapi[standard]" colorama pysocks requests free-proxy tomli pillow send2trash pytz pymediainfo gradio_client selenium

COPY ./app /code/app
RUN cp /code/app/config.toml /code/config.toml

COPY ./guzlacpn.default-release-1 /code/guzlacpn.default-release-1

RUN wget https://exiftool.org/Image-ExifTool-12.96.tar.gz
RUN tar -zxvf Image-ExifTool-12.96.tar.gz

RUN mkdir /code/app/output

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]