#importing selenium libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#importing time library
import time
import random   #Import 


chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])

driver=webdriver.Chrome(executable_path=r"\CodingProjects\navigationWeb\chromedriver.exe",chrome_options=chrome_options)
driver.get('https://ferrefaster.com/')


paginas=driver.find_elements(By.XPATH,'//a[@href]')
varcontinue=True
while varcontinue:
  link=random.choice(paginas)
  if link.is_displayed() and link.is_enabled():
    target=link.get_attribute('href')
    driver.get(target)
    varcontinue=False
print(f"{driver.title} en \n{driver.current_url}")

driver.quit()
