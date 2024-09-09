from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver import ActionChains
import os
from sys import platform
from time import sleep
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX

from rename_to_current_time import return_renamed
from img_postprocessing_logging import img_postprocessing_logging, open_folder
from unlimited_ai_img import config_data, write_to_output, now
cf = config_data()
slash = "\\" if platform == "win32" else "/"
pwd = os.getcwd()

# xpath to interact with the website
xpath: dict[str, str] = {
  "image1-downloadbtn": "/html/body/div/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div/button[2]",
  "image2-downloadbtn": "/html/body/div/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div/button[2]",
  "image3-downloadbtn": "/html/body/div/div/div/div/div[1]/div[1]/div/div[3]/div/div[1]/div[1]/div[2]/div/button[2]",
  "image4-downloadbtn": "/html/body/div/div/div/div/div[1]/div[1]/div/div[4]/div/div[1]/div[1]/div[2]/div/button[2]",
  "textbox-prompt": "/html/body/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]",
  "run": "/html/body/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/button",
  }


def profile_launch_and_login():
  
  # fetch profile path
  path_to_profile:list[str] = cf['profiles_only']

  # select 1st profile
  path_to_profile = path_to_profile[0]

  # init firefox options and profile paths
  options = Options()
  options.profile = webdriver.FirefoxProfile(path_to_profile) 
  # auto download settings
  options.profile.set_preference("browser.download.folderList", 2)
  options.profile.set_preference("browser.download.dir", f"{pwd}{slash}{cf['savepath']}")
  if not os.path.exists(cf['savepath']):  os.makedirs(cf['savepath'])
  options.profile.set_preference("browser.helperApps.neverAsk.saveToDisk","image/jpeg")
  # other firefox options (including pageload strategy and https settings)
  # options.page_load_strategy = 'eager'

  # Navigate to a URL, resize window
  driver = webdriver.Firefox(options=options)
  driver.set_window_size(1200, 900)
  driver.get(f"https://aitestkitchen.withgoogle.com/tools/image-fx")

  return driver


def get_element(xpath:str):
  while True:
    try:
      element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, xpath)))
      return element
    except TimeoutException:
      return False

  

if __name__ == "__main__":
  # launch profile and login, return driver
  driver = profile_launch_and_login()
  # init actions
  actions = ActionChains(driver)
  # insert prompt
  element = get_element(xpath['textbox-prompt'])
  actions.move_to_element(element).click().perform()
  # Send each character with a small delay
  for char in cf['prompt']:
    actions.send_keys(char).perform()
    sleep(0.05)
  # click run
  element = get_element(xpath['run'])
  element.click()

  # fetch the photo download btn
  for i in range(4):
    element = get_element(xpath[f'image{i+1}-downloadbtn'])
    if element != False: # if there is an element
      element.click()
      while True: # loop to check if the image is generated
        check = os.path.exists(f"{cf['savepath']}{slash}image_fx_.jpg")
        if check == True:
          sleep(2)
          img_postprocessing_logging(f"{cf['savepath']}{slash}image_fx_.jpg", cf['savepath'], return_renamed())
          break
        else:  sleep(0.5)
    else:  print(RED,f"Image #{i+1} no image generated",RESET)
  
  # invoke opening folder if true
  if cf['opendir_on_finish']:   open_folder(cf['savepath'])
  driver.close()