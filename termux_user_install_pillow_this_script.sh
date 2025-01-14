pip install wheel && \
pkg install libjpeg-turbo libwebp && \
LDFLAGS="-L/system/lib64/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install --no-cache-dir --force-reinstall Pillow
