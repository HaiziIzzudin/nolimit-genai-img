git clone https://github.com/HaiziIzzudin/nolimit-genai-img.git;
cd nolimit-genai-img;
docker build -t myimage .;
docker run -d --name mycontainer -p 80:80 myimage;