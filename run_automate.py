from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, request
from selenium.webdriver.chrome.service import Service
import time
import random

app=Flask(__name__,template_folder='template')

@app.route('/')
def automation():
    return render_template('automation.html')

@app.route('/automation', methods=['get','POST'])
def run_automation():
    if request.method == 'POST':
        criterio_busqueda=request.form.get('criterio_busqueda')
        urlweb=request.form.get('urlweb')
        repeticiones=int(request.form.get('repeticiones'))
        salida=navigation_web(criterio_busqueda,urlweb,repeticiones)
        return salida

def scrolling(wait,direction,step):
    screen_size=driver.execute_script("return document.body.scrollHeight")
    if direction:
        for i in range(step):
            argumento=f"window.scrollTo(0,{screen_size*((i+1)/step)})"
            driver.execute_script(argumento)
            time.sleep(wait)
    else:
        for i in range(step):
            argumento=f"window.scrollTo(0,{screen_size*(1-((i+1)/step))})"
            driver.execute_script(argumento)
            time.sleep(wait)

def googleNavigation(urlweb):
    paginas=driver.find_elements(By.PARTIAL_LINK_TEXT,'https:')
    page_exist=False
    for pagina in paginas:
        if pagina.text.find(urlweb[:-1])==-1:
            continue
        else:
            page_exist=True
            y=pagina.location['y']
            print(pagina.text)
    scrolling(2,True,10)
    time.sleep(1)
    if page_exist:
        scrolling(2,False,10)
        argument=f"window.scrollTo(0, {y})"
        driver.execute_script(argument)
        target = driver.find_element(By.PARTIAL_LINK_TEXT,urlweb[:-1])#(By.XPATH,'//a[@href="'+ urlweb[:-1] +'"]')
        driver.execute_script("arguments[0].click();", target)
    else:
        target = driver.find_element(By.ID,'pnnext')
        driver.execute_script("arguments[0].click();", target)
        page_exist=False
    return page_exist

def pageNavigation(iters):
    down=True
    for iter in range(iters):
        espera=random.randint(1,5)
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
    pageNavigation(iters)

def navigation_web(criterio_busqueda,urlweb,repeticiones):
    servicio=Service(ChromeDriverManager().install())
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach',True)
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    global driver
    for k in range(repeticiones):
        driver=webdriver.Chrome(service=servicio,chrome_options=chrome_options)
        driver.maximize_window()
        driver.get('https://google.com')
        time.sleep(1)

        input_box=driver.find_element(By.NAME,'q')
        for letra in criterio_busqueda:
            input_box.send_keys(letra)
            time.sleep(0.35)
        time.sleep(1)
        input_box.send_keys(Keys.ENTER)

        page_found=False
        while not page_found:
            page_found=googleNavigation(urlweb)
        
        navega=random.randint(1,5)
        pageNavigation(navega)
        navega_sitio=random.randint(1,5)
        navegarSitio(navega_sitio,urlweb)
        driver.close()

    driver.quit()
    return 'Se completo la navegacion'

if __name__ == '__main__':
    app.run(debug=True)

