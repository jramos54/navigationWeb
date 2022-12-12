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
    scrolling(3,True,10)
    time.sleep(.1)
#Evaluate if the url target exist in the current page
    if page_exist:
#Scrolling up
        scrolling(3,False,10)
#Scrolling to the location of url target
        argument=f"window.scrollTo(0, {y})"
        driver.execute_script(argument)
        print(f'movimiento hacia: {driver.execute_script("return window.scrollY"):.0f}')
#Click to the url target
        target = driver.find_element(By.XPATH,'//a[@href="'+ urlweb +'"]')
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
        scrolling(3,down,10)
        if down:
            down=False
        else:
            down=True
    time.sleep(4)

chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
driver=webdriver.Chrome(executable_path=r"\CodingProjects\navigationWeb\chromedriver.exe",chrome_options=chrome_options)

driver.maximize_window()
time.sleep(1)
##################################################################
#                   INPUTS                                       #
##################################################################
criterio_busqueda="Ferreterias en pachuca"
urlweb="https://ferrefaster.com/"#"https://www.nfh.com.mx/"#"https://www.ferreteriasrc.com/"#"https://ferefaster.com"
repeticiones=3

##################################################################
#                     MAIN                                       #
##################################################################
driver.get('https://google.com')

for k in range(repeticiones):
    driver.execute_script("window.open('https://www.google.com')")
    driver.switch_to.window(driver.window_handles[1])

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

    pageNavigation(3)

    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])


driver.quit()

