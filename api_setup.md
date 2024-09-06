### If you decided to use API method, there is no setup if you decided to use this with no token or account.

[Go back to main tutorial](README.md)

### But if you have HF account, we recommend adding your own token to your config file.



1. Please follow this 
[instructions](https://huggingface.co/docs/hub/en/security-tokens#how-to-manage-user-access-tokens)
on how to gather access token.

2. After copying your access token, paste it under `[token]` section, inside `token` variable, like this (encased in quotes):
```toml
[token]
token = [
  "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
]
``` 

***TIP:*** This is an array, therefore feel free to add as many **token per account** as you like.

[Go back to main tutorial](README.md)