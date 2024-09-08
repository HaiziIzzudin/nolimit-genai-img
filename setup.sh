git clone https://github.com/HaiziIzzudin/nolimit-genai-img.git && \
cd nolimit-genai-img && \
nano app/config.toml && \
docker build -t myimage . && \
docker run -d --name mycontainer -p 81:81 myimage