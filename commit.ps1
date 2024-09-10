git add .
git commit -m "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")"
git push
ssh haizi@139.162.55.58 "cd nolimit-genai-img/ && git pull"