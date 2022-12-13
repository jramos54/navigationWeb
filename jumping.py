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
links=[pagina.get_attribute('href') for pagina in paginas]

link=random.choice(links)
print(type(link),link)

validLink=True
while validLink:
    if 'http' in link:
        #element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'//a[@href="'+link+'"]')))
        #target=driver.find_element(By.XPATH,'//a[@href="'+link+'"]')
        #driver.execute_script("arguments[0].click();",target)
        target=f"window.open('{link}')"
        driver.execute(target)
        
        validLink=False
    else:
        link=random.choice(links)

driver.quit()