from time import sleep

def countdown(message: str, seconds: int):
  # how many seconds you want to wait
  while seconds >= 1:
    print(message, str(seconds) + '...', end='\r')
    sleep(1)
    seconds = seconds - 1