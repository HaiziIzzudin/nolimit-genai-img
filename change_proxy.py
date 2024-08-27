import socks
import socket
import requests
from requests import Session
import json
import random
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX
from fp.fp import FreeProxy

from unlimited_ai_img import config_data, write_to_output, now
cf = config_data()





### custom exception
class getNewIP_ModeError(Exception("Mode can only receive either 'api' or 'selenium'")):
  pass




### for testing purposes
if __name__ != '__main__':
  version = cf['proxy_finder_ver']
else:
  version = 1  ## change the value here for testing


if version == 0:  # use computer ip
  def getNewIP(mode:str = None):
    """
    mode not applicable here
    """
    socks.set_default_proxy()
    response = requests.get("http://httpbin.org/ip", timeout=2.5) # seconds
    if response.status_code == 200: ## OK
      response = json.loads(response.text)
      response = f"Connected to local computer {response['origin']} 🛜"
      write_to_output('ip', response['origin'])
      print(GREEN, response, RESET)
    return

elif version == 1:
  def getNewIP(mode:str):
    """
    mode can be 'api' | 'selenium': returns dict 'proxy_url' and 'socks_ver'
    """
    while True: # loop until breaks
      # disconnect from malfunctioned proxy
      socks.set_default_proxy()
      proxy_lists = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.json'
      write_to_output('proxy_lists', proxy_lists)
      response = requests.get(proxy_lists)
      data = json.loads(response.content)

      while True: # loop until breaks
        rand = random.randint(0, (len(data) - 1))
        write_to_output('proxy_data_count', len(data))
        write_to_output('lucky_number', rand)
        
        proxy_url = data[rand]["proxy"]
        protocol = data[rand]["protocol"]
        ip = data[rand]["ip"]
        port = data[rand]["port"]
        write_to_output('proxy_url', proxy_url)
        write_to_output('protocol', protocol)
        write_to_output('ip', ip)
        write_to_output('port', port)

        try:
          print(YELLOW, f"Connecting to proxy {ip}...", RESET)
          write_to_output('connection_testing_begin', now())

          if (protocol == 'socks5'):
            socks.set_default_proxy(socks.SOCKS5, ip, port)
            socket.socket = socks.socksocket
          
          elif (protocol == 'socks4'):
            socks.set_default_proxy(socks.SOCKS4, ip, port)
            socket.socket = socks.socksocket

          elif (protocol == 'http'):
            session = Session()
            session.proxies.update({'http': proxy_url})

          # Now all socket connections will go through their respective protocols and proxies
          response = requests.get("http://httpbin.org/ip", timeout=1.5) # seconds
          break

        except:
          write_to_output('connection_testing_end', now())
          write_to_output('connection_testing_status', 'failed', True)
          print(MAGENTA,"We're having some problems connecting with the proxy. Retrying with other proxy...",RESET)

      if response.status_code == 200: ## OK
        ip_connected_to = json.loads(response.text)
        write_to_output('connection_testing_end', now())
        write_to_output('connection_testing_status', 'success')
        print(GREEN, f"Connected to proxy {ip_connected_to['origin']} 🛜", RESET)
        break
      else:
        write_to_output('connection_testing_end', now())
        write_to_output('connection_testing_status', 'failed', True)
        print(YELLOW, "Proxy unresponsive. Changing proxy...", RESET)

    if mode == 'selenium':
      socks.set_default_proxy()
      if (protocol == 'socks5'):
        return {
          'proxy_url': f'{ip}:{port}',
          'socks_ver': 5
          }
      if (protocol == 'socks4'):
        return {
          'proxy_url': f'{ip}:{port}',
          'socks_ver': 4
          }
      elif (protocol == 'http'):
        return {
          'proxy_url': proxy_url.replace("http://", ""),
          'socks_ver': 'http'}
    elif mode == 'api':   return
    else:   raise getNewIP_ModeError



elif version == 2:
  def getNewIP(mode:str):
    """
    mode can be 'api' | 'selenium': returns dict 'proxy_url' and 'socks_ver'
    """
    proxy_url = FreeProxy(rand=True).get()
    if mode == 'api':
      session = Session()
      session.proxies.update({'http': proxy_url})
      response = f"Connected to proxy {proxy_url.replace('http://','')} 🛜"
      write_to_output('proxy_url', proxy_url)
      print(GREEN, response, RESET)
    elif mode == 'selenium':
      return {
          'proxy_url': proxy_url.replace("http://", ""),
          'socks_ver': 'http'
          }
    else:
      raise getNewIP_ModeError
    




if __name__ == '__main__':
  print(f"Version: {version}")
  print( getNewIP('api') )
