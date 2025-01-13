pip install wheel && \
pkg install libjpeg-turbo && \
LDFLAGS="-L/system/lib64/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install Pillow