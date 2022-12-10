from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

def scrolling(wait,direction,step):
    screen_size=driver.execute_script("return document.body.scrollHeight")
    if direction:
        for i in range(step):
            argumento=f"window.scrollTo(0,{screen_size*((i+1)/step)})"
            driver.execute_script(argumento)
            print(f"movimiento hacia abajo en Posicion: {driver.execute_script('return window.scrollY'):.0f}")
            time.sleep(wait)
    else:
        for i in range(step):
            argumento=f"window.scrollTo(0,{screen_size*(1-((i+1)/step))})"
            driver.execute_script(argumento)
            print(f"movimiento hacia arriba en posicion: {driver.execute_script('return window.scrollY'):.0f}")
            time.sleep(wait)

def googleNavigation(urlweb):
    paginas=driver.find_elements(By.PARTIAL_LINK_TEXT,'https:')
    page_exist=False
    for pagina in paginas:
        print(f"{pagina.text}")
        if pagina.text.find(urlweb[:-1])==-1:
            continue
        else:
            page_exist=True
            y=pagina.location['y']
            print(f"{pagina.location} > {pagina.text}")
    scrolling(3,True,10)
    time.sleep(.1)
    if page_exist:
        scrolling(3,False,10)
        argument=f"window.scrollTo(0, {y})"
        driver.execute_script(argument)
        print(f'movimiento hacia: {driver.execute_script("return window.scrollY"):.0f}')
        target = driver.find_element(By.XPATH,'//a[@href="'+ urlweb +'"]')
        driver.execute_script("arguments[0].click();", target)
    else:
        target = driver.find_element(By.ID,'pnnext')
        driver.execute_script("arguments[0].click();", target)
        page_exist=False
    return page_exist

def pageNavigation(times):
    down=True
    for time in range(times):
        scrolling(3,down,10)
        if down:
            down=False
        else:
            down=True
    time.sleep(4)

chrome_options=webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('detach',True)
driver=webdriver.Chrome(executable_path=r"\CodingProjects\navigationWeb\chromedriver.exe",chrome_options=chrome_options)

driver.maximize_window()
time.sleep(1)

criterio_busqueda="Ferreterias en pachuca"
urlweb="https://ferrefaster.com/"#"https://www.nfh.com.mx/"#"https://www.ferreteriasrc.com/"#"https://ferefaster.com"
repeticiones=3

driver.get('https:/google.com')
print(f"Se accedio a: {driver.title}\nEn la url: {driver.current_url} ")
time.sleep(1)

input_box=driver.find_element(By.NAME,"q")
for letra in criterio_busqueda:
    input_box.send_keys(letra)
    time.sleep(.35)
#input_box.send_keys(criterio_busqueda)
print(f"Se ingreso el criterio de busqueda: {criterio_busqueda}")
time.sleep(2)
input_box.send_keys(Keys.ENTER)
print(f"Resultados del criterio de busqueda: {criterio_busqueda}\n{driver.title}")

page_found=False
while not page_found:
    page_found=googleNavigation(urlweb)

print(f"Se ingreso a la pagina: {driver.title}\nEn url: {driver.current_url}")

pageNavigation(5)

driver.quit()

