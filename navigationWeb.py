"""
Web navigation app
by: Joel Ramos Molina
email: jrmsmolina54@gmail.com
This app navigate thru google by using a key search and look for a web page target
when the target is found in the page, it navigates to the target webpage
the app navigates into the target webpage by n times defined by user
the operation is repeated by k times defined by user
"""

#importing selenium libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#importing time library
import time
import random   #Import random from changues required on 12/12/22
import os
import stem.process
import re
import urllib.request
from datetime import datetime
from fake_useragent import UserAgent


#defining functions to be used
def scrolling(wait,direction,step):
    """
    this function provides the scrolling thru the webpage
    wait >> is the time in seconds the scrolling will delay
    direction >> if True scroll down, if False Scroll up
    step >> is the n steps the scroll will be executed i.e. if defined 4, will happen 4 scroll
    with 4 delays
    """
#To get the screen size
    screen_size=driver.execute_script("return document.body.scrollHeight")
#Evaluates the direction of the scroll
    if direction:
        for i in range(step):
 #evaluate the size of the scroll, it is if size is 100 and step 4, the scroll is 25
            argumento=f"window.scrollTo(0,{screen_size*((i+1)/step)})"
            driver.execute_script(argumento)
            print(f"movimiento hacia abajo en Posicion: {driver.execute_script('return window.scrollY'):.0f}")
            time.sleep(wait)
    else:
        for i in range(step):
 #evaluate the size of the scroll, it is if size is 100 and step 4, the scroll is 25
            argumento=f"window.scrollTo(0,{screen_size*(1-((i+1)/step))})"
            driver.execute_script(argumento)
            print(f"movimiento hacia arriba en posicion: {driver.execute_script('return window.scrollY'):.0f}")
            time.sleep(wait)

def googleNavigation(urlweb):
    """
    This function provide the google navigation after search
    urlweb >> is the url target
    the function will shows in the console the searched webpages
    """
#To get the webpages in the search, it doesnt includes adversiting
    paginas=driver.find_elements(By.PARTIAL_LINK_TEXT,'https:')
    page_exist=False
#To show the pages and look for the url targer if is in this page
    for pagina in paginas:
        print(f"{pagina.text}")
        if pagina.text.find(urlweb[:-1])==-1:
            continue
        else:
            page_exist=True
            y=pagina.location['y']
            print(f"{pagina.location} > {pagina.text}")
#scrolling down
    scrolling(2,True,10)
    time.sleep(.1)
#Evaluate if the url target exist in the current page
    if page_exist:
#Scrolling up
        scrolling(2,False,10)
#Scrolling to the location of url target
        argument=f"window.scrollTo(0, {y})"
        driver.execute_script(argument)
        print(f'movimiento hacia: {driver.execute_script("return window.scrollY"):.0f}')
#Click to the url target
        target = driver.find_element(By.PARTIAL_LINK_TEXT,urlweb[:-1])#(By.XPATH,'//a[@href="'+ urlweb[:-1] +'"]')
        driver.execute_script("arguments[0].click();", target)
    else:
#clcik to the next button in google page
        target = driver.find_element(By.ID,'pnnext')
        driver.execute_script("arguments[0].click();", target)
        page_exist=False
    return page_exist

def pageNavigation(iters):
    down=True
    for iter in range(iters):
        espera=random.randint(1,5)
        print(f'Las esperas son de {espera} segundos')
        scrolling(espera,down,10) # Segenera el random entre 1 y 5 para las pausas del scrolling
        if down:
            down=False
        else:
            down=True
    time.sleep(1)

def navegarSitio(iters,urlweb):
    
    paginas=driver.find_elements(By.XPATH,'//a[@href]')
    varcontinue=True
    while varcontinue:
      link=random.choice(paginas)
      if link.is_displayed() and link.is_enabled():
        target=link.get_attribute('href')
        if urlweb in target:
            driver.get(target)
            varcontinue=False

    print(f"{driver.title} en \n{driver.current_url}")

    pageNavigation(iters)

##########################################
#            CONSTANTS
##########################################
SOCKS_PORT=9050
PATH_TORBROWSER=os.path.normpath(os.getcwd()+'\\torbrowser\\tor\\tor.exe')
PATH_GEOIP=os.path.normpath(os.getcwd()+'\\torbrowser\\data\\geoip')
PATH_CHROME=os.path.normpath(os.getcwd()+'\\torbrowser\\chromedriver.exe')
##########################################
#             TOR LOCATIONS
#########################################
try:
    urllib.request.urlretrieve('https://raw.githubusercontent.com/torproject/tor/main/src/config/geoip',PATH_GEOIP)
except:
    print('no se pudo conectar')
##########################################
#         TOR CONFIGURATION
##########################################
tor_process=stem.process.launch_tor_with_config(
    config={
        'SocksPort':str(SOCKS_PORT),
        'EntryNodes':'{US}',
        'ExitNodes':'{MX}',
        'StrictNodes':'1',
        'CookieAuthentication':'1',
        'MaxCircuitDirtiness':'60',
        'GeoIPFile':PATH_GEOIP,
    },
    init_msg_handler=lambda line:print(line) if re.search('Bootstrapped',line) else False,
    tor_cmd=PATH_TORBROWSER
)
##########################################
#       PROXIES
##########################################
PROXIES={
    'http':'socks5://127.0.0.1:9050',
    'https':'socks5://127.0.0.1:9050'
}
PROXY='socks5://localhost:9050'
##########################################
#             CHROME CONFIGURATION
##########################################
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
chrome_options.add_argument('--proxy-server=%s'%PROXY)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#driver=webdriver.Chrome(executable_path=r"\CodingProjects\navigationWeb\chromedriver.exe",chrome_options=chrome_options)
#options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
chrome_options.add_argument(f'user-agent={userAgent}')

##################################################################
#                   INPUTS                                       #
##################################################################
criterio_busqueda=input('ingresa el criterio de busqueda:\t ')
urlweb=input('ingresa la URL del sitio:\t ')#"https://ferrefaster.com/"#"https://www.nfh.com.mx/"#"https://www.ferreteriasrc.com/"#"https://ferefaster.com"
numerico=True
while numerico:
    try:
        repeticiones=int(input('ingresa el numero de veces que se repite el proceso:\t '))#2
        numerico=False
    except:
        print('por favor ingresa un numero')
##################################################################
#                     MAIN                                       #
##################################################################

for k in range(repeticiones):
    #Se abre el navegador al incio del ciclo
    driver=webdriver.Chrome(executable_path=PATH_CHROME,chrome_options=chrome_options)
    driver.get('https://google.com')
    driver.maximize_window()
    time.sleep(1)
   
    print(f"Se accedio a: {driver.title}\nEn la url: {driver.current_url} ")
    time.sleep(1)

    input_box=driver.find_element(By.NAME,"q")
    for letra in criterio_busqueda:
        input_box.send_keys(letra)
        time.sleep(.35)
    print(f"Se ingreso el criterio de busqueda: {criterio_busqueda}")
    time.sleep(2)
    input_box.send_keys(Keys.ENTER)
    print(f"Resultados del criterio de busqueda: {criterio_busqueda}\n{driver.title}")

    page_found=False
    while not page_found:
        page_found=googleNavigation(urlweb)

    print(f"Se ingreso a la pagina: {driver.title}\nEn url: {driver.current_url}")
    navega=random.randint(1,5)
    print(f'Se navegara {navega} veces')
    pageNavigation(navega) #se genera el random entre 1y 5 para el numero de veces que navega
    ########################################################
    #   se navega en pagina aleatoria del sitio            #
    ########################################################
    navega=random.randint(1,5)
    navegarSitio(navega,urlweb)
    driver.close() # Se cierra el navegador al final de la navegacion
    time.sleep(1)

tor_process.kill()
driver.quit() 

print('se finalizo la navegacion')
