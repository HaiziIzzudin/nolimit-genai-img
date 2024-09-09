from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from time import sleep
import re
from os.path import exists as file_exists
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX

from rename_to_current_time import return_renamed
from img_postprocessing_logging import img_postprocessing_logging, open_folder
from change_proxy import getNewIP
from raw import convert2raw
from unlimited_ai_img import config_data, write_to_output, now
cf = config_data()



# xpath to interact with the website
xpath: dict[str, str] = {
  "iframe": '//*[@id="iFrameResizer0"]',
  "prompt_field": "/html/body/gradio-app/div/div/div[1]/div/div/div/div[2]/div/label/input",
  "advanced_settings": "/html/body/gradio-app/div/div/div[1]/div/div/div/div[4]/button",
  "width": "/html/body/gradio-app/div/div/div[1]/div/div/div/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/div/input",
  "height": "/html/body/gradio-app/div/div/div[1]/div/div/div/div[4]/div[2]/div/div[2]/div/div[2]/div[2]/div/input",
  "inference": "/html/body/gradio-app/div/div/div[1]/div/div/div/div[4]/div[2]/div/div[3]/div/div[2]/div[2]/div/input",
  "run": '//*[@id="component-5"]',
  "progress_value": "/html/body/gradio-app/div/div/div[1]/div/div/div/div[3]/div[1]/div[1]",
  "image_results": '/html/body/gradio-app/div/div/div[1]/div/div/div/div[3]/button/div/img',
  "image_in_new_tab": '/html/body/img',
  "download_btn": '/html/body/gradio-app/div/div/div[1]/div/div/div/div[3]/div[2]/a/button',
  "err": '/html/body/gradio-app/div/div/div[1]/div/div/div/div[3]/div[1]/span',
  }



def firefoxInit_and_webpageLaunch(k:int):
  """
  this def will return `driver` variable, which you can pass to the subsequent def

  first, let's test if user logged in profile is able to generate image,
  if not, try with another,
  if not, try with another,
  until it come to false, where we can use private browsing mode.
  """

  def additional_settings():
    options.profile.set_preference("browser.privatebrowsing.autostart", True)
    
    # get new proxy ip and port
    proxy_info = getNewIP('selenium')
    socks_ver, proxy_url = proxy_info['socks_ver'], proxy_info['proxy_url']
    print(Fore.YELLOW, f"Configuring proxy {socks_ver} {proxy_url} to webdriver...", Style.RESET_ALL)
    if socks_ver == 'http':
      options.proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'httpProxy' : proxy_url})
    elif (socks_ver == 5) or (socks_ver == 4):
      options.proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'socksProxy' : proxy_url, 'socksVersion' : socks_ver})
    
    options.profile.set_preference('webdriver_assume_untrusted_issuer', False)
    options.profile.set_preference("browser.download.manager.showWhenStarting", False)
    options.profile.set_preference("security.enterprise_roots.enabled", True)


  while True:
    
    hf_logged_in = cf['profiles'][k][0]
    path_to_profile = cf['profiles'][k][1]
    
    # init firefox options and profile paths
    options = Options()
    options.profile = webdriver.FirefoxProfile(path_to_profile) 
    # auto download settings
    options.profile.set_preference("browser.download.folderList", 2)
    options.profile.set_preference("browser.download.dir", cf['savepath'])
    options.profile.set_preference("browser.helperApps.neverAsk.saveToDisk","image/webp")
    # other firefox options (including pageload strategy and https settings)
    options.page_load_strategy = 'eager'
    options.set_preference("network.websocket.allowInsecureFromHTTPS", True)
    options.set_preference("dom.security.https_only_mode", False)
    options.set_preference("security.fileuri.strict_origin_policy", False)
    options.set_preference("security.csp.enable", True)

    if hf_logged_in == False:
      additional_settings()
    elif hf_logged_in == True:
      k += 1
    
    # Navigate to a URL, resize window
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(850, 850)
    try:
      driver.get(f"https://huggingface.co/spaces/{cf['model_name']}")
      break
    except Exception:
      print(RED,'Server has rejected connections. Reinitializing...',RESET)
      driver.close()
      continue

  return {
    'driver': driver,
    'k': k
    }


def navigate_to_xpath(driver):
  """
  Navigate to the specified XPath in the webpage, switch to the iframe, 
  enter the prompt, open advanced settings, and set the width, height, and 
  inference count. Returns True if successful, False if a TimeoutException 
  occurs.

  Parameters:
    None

  Returns:
    bool: Whether the navigation and settings update were successful
  """
  
  try:
    ### wait until iframe exists, then switch to it.
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath["iframe"])))
    driver.switch_to.frame(iframe)
    print(MAGENTA,'Switched selenium control to iframe',RESET)

    ### wait until prompt_field exists, then grab the webelement.
    # at this point all gradio elemnt has been loaded
    prompt_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath["prompt_field"])))
    if prompt_field.is_displayed():   prompt_field.send_keys(cf['prompt'])
  
  except TimeoutException:
    print(RED,'Host took too long to respond. Switching to another instances...',RESET)
    driver.quit()
    return False

  # open advanced settings
  element = driver.find_element(By.XPATH, xpath["advanced_settings"])
  element.click()

  # change value of width and height and inference to specified value
  element = driver.find_element(By.XPATH, xpath["width"])
  element.clear()
  element.send_keys(cf['width'])
  element = driver.find_element(By.XPATH, xpath["height"])
  element.clear()
  element.send_keys(cf['height'])
  element = driver.find_element(By.XPATH, xpath["inference"])
  element.clear()
  element.send_keys(cf['inference_count'])

  return True
  

def begin_inferencing(run_number: int, driver):

  # give notice first to user
  print(MAGENTA,f"Run #{run_number+1}.\nHF + selenium free compute yields longer results. Please be patient...",RESET)

  # finally, click run.
  element = driver.find_element(By.XPATH, xpath["run"])
  element.click()

  # generate new filename
  filename_no_ext: str = return_renamed()

  # try if huggingface throw err on their web ui, catch it, and return False
  # else continue with the instructions
  try:
    # err will come out almost immediately, therefore timeout value should be low
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath["err"])))
    print(MAGENTA,'Image generation error, possibly due to rate limiting. Please hold as we move you to another instance...',RESET)
    driver.quit()
    return (False, filename_no_ext)
  
  except TimeoutException:
    while True: # this is for progress updates for every 0.1 seconds
      try:
        progress = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath["progress_value"])))
        progress_text = progress.text
        
        # use regex to get only the seconds. Example can be:
        # "12/25 steps |   15.2/43.5s" OR "15.2/43.5s" OR "processing | 15.2/43.5s"
        match = re.findall(r'(\d\.\d)\/(\d\.\d)s', progress_text)
        if match:
          progress_current, progress_total = float(match[0]), float(match[1])
          print(YELLOW,f"Image is generating. ETA: {(progress_total - progress_current):.1f} seconds left",RESET, end="\r")
        else:
          print(YELLOW,f"Image is generating. Please wait...",RESET, end="\r")
        sleep(0.1)
      except TimeoutException:  break# image successfully created. proceeding...

    # click to download the picture
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath["image_results"])))
    img_dl_btn = driver.find_element(By.XPATH, xpath["download_btn"])
    img_dl_btn.click()
    sleep(2)  ## if you have a slow connection, consider upping this value

    # postprocess photo
    img_postprocessing_logging(f"{cf['savepath']}\\image.webp", cf['savepath'], filename_no_ext)
    
    # Initialize the ActionChains object
    # actions = ActionChains(driver)
    # Perform the action to press the Escape key
    # actions.send_keys(Keys.ESCAPE).perform()

    return (True, filename_no_ext)









############
### MAIN ###
############

if __name__ == '__main__':
  # indication to user of their prompt
  print('Prompt:\n', cf['prompt'])

  k = 0
  while True:
    # assign driver return to driver var
    firefoxInit = firefoxInit_and_webpageLaunch(k)
    driver = firefoxInit['driver']  ## driver is tuple
    k = firefoxInit['k']
    # kita dah declare global variable driver, therefore dah x perlu pass driver var to other def
    conn_status = navigate_to_xpath(driver)
    if conn_status == True:
      break

  i = 0
  while i < cf['gen_count']:
    infer_status = begin_inferencing(i, driver)
    write_to_output('hf_model', cf['model_name'])
    write_to_output('prompt', cf['prompt'])
    write_to_output('prompt', cf['prompt'])
    write_to_output('img_output_width', cf['width'])
    write_to_output('img_output_height', cf['height'])
    write_to_output('inference_steps', cf['inference_count'])
    write_to_output('inference_steps', cf['inference_count'])
    write_to_output('model_inference_begin', now())

    if infer_status[0] == False:
      write_to_output('model_inference_end', now())
      write_to_output('model_inference_status', 'failed')
      write_to_output('model_inference_reason', 'Image generation error, possibly due to rate limiting. Please hold as we move you to another instance...', True)
      
      while True:
        # assign driver return to driver var
        firefoxInit = firefoxInit_and_webpageLaunch(k)
        driver = firefoxInit['driver']  ## driver is tuple
        k = firefoxInit['k']
        # kita dah declare global variable driver, therefore dah x perlu pass driver var to other def
        conn_status = navigate_to_xpath(driver)
        if conn_status == True:
          break

    elif infer_status[0] == True:
      write_to_output('model_inference_end', now())
      write_to_output('model_inference_status', 'success')
      write_to_output('img_new_filename', infer_status[1]+'.jpg')
      write_to_output('img_download_status', 'success', True)
      i += 1


  # invoke opening folder if true
  if cf['opendir_on_finish']:   open_folder(cf['savepath'])
  driver.close()