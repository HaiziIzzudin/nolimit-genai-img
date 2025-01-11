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

if __name__ != '__main__':
  from toml_ingest import config_data
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
      response = requests.get(proxy_lists)
      data = json.loads(response.content)

      while True: # loop until breaks
        rand = random.randint(0, (len(data) - 1))
        proxy_url = data[rand]["proxy"]
        protocol = data[rand]["protocol"]
        ip = data[rand]["ip"]
        port = data[rand]["port"]

        try:
          print(YELLOW, f"Connecting to proxy {ip}...", RESET)

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
          print(MAGENTA,"We're having some problems connecting with the proxy. Retrying with other proxy...",RESET)

      if response.status_code == 200: ## OK
        ip_connected_to = json.loads(response.text)
        print(GREEN, f"Connected to proxy {ip_connected_to['origin']} 🛜", RESET)
        break
      else:
        print(YELLOW, "Proxy unresponsive. Changing proxy...", RESET)

    if mode == 'selenium':
      socks.set_default_proxy()
      if (protocol == 'socks5'):
        return {
          'proxy_url': f'{ip}:{port}',
          'socks_ver': 5
          }
      elif (protocol == 'socks4'):
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
      print(GREEN, response, RESET)
    elif mode == 'selenium':
      return {
          'proxy_url': proxy_url.replace("http://", ""),
          'socks_ver': 'http'
          }
    else:
      raise getNewIP_ModeError
    




if __name__ == '__main__':
  proxy_info = getNewIP('api')
  
  
  # func to launch firefox
  from selenium import webdriver
  from selenium.webdriver.common.proxy import Proxy, ProxyType
  from selenium.webdriver.firefox.options import Options
  
  # init firefox options and profile paths
  options = Options()
  # SSL allow settings
  options.set_preference("network.websocket.allowInsecureFromHTTPS", True)
  options.set_preference("dom.security.https_only_mode", False)
  options.set_preference("security.fileuri.strict_origin_policy", False)
  options.set_preference("security.csp.enable", True)

  options.set_preference("browser.privatebrowsing.autostart", True)
    
  # get new proxy ip and port
  proxy_info = getNewIP('selenium')
  socks_ver, proxy_url = proxy_info['socks_ver'], proxy_info['proxy_url']
  print(Fore.YELLOW, f"Configuring proxy {socks_ver} {proxy_url} to webdriver...", Style.RESET_ALL)
  if socks_ver == 'http':
    options.proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'httpProxy' : proxy_url})
  elif (socks_ver == 5) or (socks_ver == 4):
    options.proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'socksProxy' : proxy_url, 'socksVersion' : socks_ver})
  
  options.set_preference('webdriver_assume_untrusted_issuer', False)
  options.set_preference("browser.download.manager.showWhenStarting", False)
  options.set_preference("security.enterprise_roots.enabled", True)

  # Navigate to a URL, resize window
  driver = webdriver.Firefox(options=options)
  driver.get(f"https://vocalremover.org/")
