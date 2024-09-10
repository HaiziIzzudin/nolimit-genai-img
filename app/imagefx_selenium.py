import base64
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
from countdown import countdown
cf = config_data()
slash = "\\" if platform == "win32" else "/"
pwd = os.getcwd()

# xpath to interact with the website
# xpath: dict[str, str] = {

#   }

def xpath(count:int=1):
  return {
    "image-dlbtn": f"/html/body/div/div/div/div/div[1]/div[1]/div/div[{count}]/div/div[1]/div[1]/div[2]/div/button[2]",
              "err": f"/html/body/div/div/div/div/div[1]/div[1]/div/div[{count}]/h3",
    "textbox-prompt": "/html/body/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]",
              "run": "/html/body/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/button",
  }




def profile_launch_and_login(headless:bool=False):
  
  # fetch profile path
  path_to_profile:list[str] = cf['profiles_only']

  # select 1st profile
  path_to_profile = path_to_profile[0]

  # init firefox options and profile paths
  options = Options()
  if headless:  options.add_argument("-headless")
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


def get_element(driver:webdriver, xpath:str):
  while True:
    try:
      element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
      return element
    except TimeoutException:
      return False




############
### MAIN ###
############

class main():
  
  def init_driver(self, headless:bool):
    # launch profile and login, return driver
    self.driver = profile_launch_and_login(headless)
    # init actions
    self.actions = ActionChains(self.driver)
    print(GREEN,'Profile launched and logged in',RESET)
  
  def run(self, prompt:str):
    driver = self.driver
    actions = self.actions
    # insert prompt
    element = get_element(driver, xpath()['textbox-prompt'])
    actions.move_to_element(element).click().perform()
    # Send each character with a small delay
    for char in prompt:
      actions.send_keys(char).perform()
      sleep(0.05)
    # click run
    element = get_element(driver, xpath()['run'])
    element.click()
    print(GREEN,'Prompt inserted and run button clicked',RESET)

    # init list to store image names, and wait for infer to finish
    self.image_list:list[str] = []
    countdown("Waiting for infer to done in", 30)

    # fetch the photo download btn
    for i in range(4):
      element = get_element(driver, xpath(i+1)["image-dlbtn"])
      if element != False: # if there is an element
        element.click()
        while True: # loop to check if the image is generated
          check = os.path.exists(f"{cf['savepath']}{slash}image_fx_.jpg")
          if check == True:
            sleep(2)
            newname_noext = return_renamed()
            img_postprocessing_logging(f"{pwd}{slash}{cf['savepath']}{slash}image_fx_.jpg", cf['savepath'], newname_noext)
            self.image_list.append(f"{pwd}{slash}{cf['savepath']}{slash}{newname_noext}.jpg")
            break
          else:  sleep(0.5)
      else:  print(RED,f"Image #{i+1} no image generated",RESET)

    driver.close()


  def return_base64(self):
    image_base64_list:list[str] = []
    for img in self.image_list:
      with open(img, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')
        image_base64_list.append(image_base64)
    return image_base64_list





def return_for_api(prompt:str):  # for fastapi
  mainprogram = main()
  mainprogram.init_driver(headless=True)
  mainprogram.run(prompt)
  data = mainprogram.return_base64()
  return data, len(data) # count from 1



if __name__ == "__main__":
  mainprogram = main()
  mainprogram.init_driver(headless=True)
  mainprogram.run(cf['prompt'])
  
  # invoke opening folder if true
  if cf['opendir_on_finish']:   open_folder(cf['savepath'])