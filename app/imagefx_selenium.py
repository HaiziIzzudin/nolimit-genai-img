from base64 import b64encode
from uuid import uuid4 as uuid
from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import os
from random import randint
from sys import platform
from time import sleep
from colorama import Fore, Style
RESET = Style.RESET_ALL
GREEN, YELLOW, RED, MAGENTA = Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.LIGHTMAGENTA_EX

from img_postprocessing_logging import img_pp, open_folder
from unlimited_ai_img import config_data
from countdown import countdown
cf = config_data()

slash = "\\" if platform == "win32" else "/"

pwd = os.getcwd()
home = os.path.expanduser("~")


def xpath(count:int=1):
  return {
    "antibot-btn": f"/html/body/div/div/div/div/form/button",
    "home-imagefx-btn": f"/html/body/div/div/div/div[2]/div[2]/div/div[3]/a",

    "google-signin-btn": f"/html/body/div/div/div/div/div[2]/div[2]/div/span/button",

    "image-dlbtn": f"/html/body/div/div/div/div/div[1]/div[1]/div/div[{count}]/div/div[1]/div[1]/div[2]/div/button[2]",
              "err": f"/html/body/div/div/div/div/div[1]/div[1]/div/div[{count}]/h3",
    "textbox-prompt": "/html/body/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div[1]",
              "run": "/html/body/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/button",
  }




class initdriver:
  def __init__(self, headless:bool = False):
    
    print(GREEN,"pwd:",pwd,RESET)
    print(GREEN,"Firefox download dir:",f"{pwd}{slash}output",RESET)

    # selecting random profiles
    if platform == "win32":
      profiles = [
        home+"\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\guzlacpn.default-release-1",
        home+"\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qy1zdxsm.default-release"
        ]
    else:
      profiles = ["/code/profile1", "/code/profile2"]

    profile_select = profiles[randint(0, len(profiles)-1)]
    print(GREEN,"Firefox profile path:",profile_select,RESET)

    # after that, we init firefox options
    options = Options()
    if headless:  options.add_argument("-headless")
    options.profile = webdriver.FirefoxProfile(profile_select) 
    # auto download settings
    options.profile.set_preference("browser.download.folderList", 2)
    options.profile.set_preference("browser.download.dir", f"{pwd+slash}output")
    if not os.path.exists(f"{pwd+slash}output"):  os.makedirs(f"{pwd+slash}output")

    # Navigate to a URL, resize window
    self.driver = webdriver.Firefox(options=options)
    self.driver.set_window_size(1200, 900)
    self.driver.get(f"https://aitestkitchen.withgoogle.com")
    print(GREEN,"Navigated to 'aitestkitchen.withgoogle.com'",RESET)

  def get_element(self, xpath:str):
    element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return element






############
### MAIN ###
############


class mainprogram:
  def __init__(self, prompt:str):
    # navigate to imagefx
    m = initdriver(headless=(platform != "win32"))
    act = ActionChains(m.driver)
    xp = xpath()
    try: # check if antibot button exists
      element = m.get_element(xp['antibot-btn'])
      act.move_to_element(element).click().perform()
      print(YELLOW,'antibot button found. Clicked!',RESET)
    except:
      print(GREEN,'antibot button not found. Proceeding...',RESET)

    # click imagefx btn
    element = m.get_element(xp['home-imagefx-btn'])
    element.click()
    print(GREEN,'<a> imagefx button clicked',RESET)

    # test google sign in blocking
    try:
      element = m.get_element(xp['google-signin-btn'])
      print(RED,'Sign in button found! Exiting...',RESET)
      m.driver.close()
      exit(2)
    except Exception as e:
      print(GREEN,'Sign in button not found. Proceeding...',RESET)

    # main infer
    element = m.get_element(xp['textbox-prompt'])
    act.move_to_element(element).click().perform()
    print(GREEN,'Inserting Prompt',RESET)

    # Send prompt
    element.send_keys(prompt)
    print(GREEN,'Prompt inserted',RESET)

    # click run
    element = m.get_element(xp['run'])
    element.click()
    print(GREEN,'run button clicked',RESET)

    # now we wait for the image to be generated
    countdown("Waiting for infer to done in", 20)

    # init list to store image names
    self.img_base64_list:list[str] = []

    # fetch the photo download btn
    for i in range(4):
      xp = xpath(i+1)
      try: # if there is download btn, click it
        element = m.get_element(xp['image-dlbtn'])
        element.click()
        sleep(3) # wait for download
        # convert image binary to base64
        with open(f"{pwd+slash}output{slash}image_fx_.jpg", "rb") as image_file:
          image_data = image_file.read()
          img_base64 = b64encode(image_data).decode('utf-8')
          self.img_base64_list.append(img_base64)
        # postprocess image
        img_pp(f"{pwd+slash}output{slash}image_fx_.jpg")
        print(GREEN,f"Image #{i+1} generated. Downloaded.",RESET)
      except (TimeoutException, NoSuchElementException) as e: # there is no element
        print(RED,e,RESET)
        print(RED,f"Image #{i+1} no image generated",RESET)
        continue

    m.driver.close()

  def return_base64(self):
    """
    Return a list of base64 strings of generated images.

    Returns:
        list[str]: A list of base64 strings of generated images.
    """
    return self.img_base64_list
  
  def return_forlocal(self):
    open_folder(f"{pwd+slash}output")




if __name__ == "__main__":
  m = mainprogram(input("Enter prompt: "))
  filename = f"{pwd+slash}{uuid()}.txt"
  with open(filename, "w") as f:
    f.write("\n".join(m.return_base64()))
  print(GREEN,f"Base64 written to {filename}",RESET)
  m.return_forlocal()