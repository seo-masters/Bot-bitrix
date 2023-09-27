from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from skpy import Skype
import sqlite3
import time
import datetime

intervalo_minutos = 15

while True:

    conexion = sqlite3.connect('bitrix_bot.db')
    cursor = conexion.cursor()         
    cursor.execute('CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, employee TEXT, phone TEXT, call_date TEXT, status TEXT, day TEXT)')

    #Esto recolecta las fechas
    fecha_actual = datetime.datetime.now()
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y")

    #Inicio de sesion en skype
    slogin = Skype("cs009@skycellular.net","aztecaintvalentina2019")
    #Perfil Objetivo
 
    options = webdriver.ChromeOptions()
    options.service_args = ['--executable_path=C:\driver_chrome\chromedriver.exe']

    # Inicio en el login 
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.bitrix24.co/")
    driver.maximize_window()

    # Encuentra la sona de inicio de sesion
    buttonLogin = driver.find_element(By.CLASS_NAME, "portal-auth-bitrix24__user")
    buttonLogin.click()
    time.sleep(1)

    # Boron de ingreso al Login
    buttonLogin = driver.find_element(By.CSS_SELECTOR, "div.bx-ui-button.bx-ui-button_primary")
    buttonLogin.click()
    time.sleep(10)

    # Obtiene el contexto de las ventanas
    ventanas = driver.window_handles

    # Cambiar el enfoque a la ventana emergente
    driver.switch_to.window(ventanas[-1])  

    # Busqueda de campo para correo
    user = driver.find_element(By.ID, "login")
    user.send_keys("contratosazteca2023@gmail.com")
    time.sleep(1)

    # Envio siguiente 
    buttonNext = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
    buttonNext.send_keys(Keys.ENTER)
    time.sleep(1)

    #Ingreso de la contraseñas
    password = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-field-input")
    password.send_keys('Botanicas2023/isidro')
    time.sleep(1)

    # Envio siguiente para volver a la web principal
    buttonNext = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
    buttonNext.click()
    time.sleep(5)

    # Vuelve a la ventana principal
    driver.switch_to.window(ventanas[0])  

    # Ingreso al listado de cuentas
    buttonAccountsList = driver.find_element(By.CLASS_NAME, "portal-auth-bitrix24__inner")
    buttonAccountsList.click()
    time.sleep(1)

    account = driver.find_element(By.CSS_SELECTOR, 'a[href="https://boxmarkcrm.bitrix24.com/"]')
    account.click()
    time.sleep(5)

    driver.get("https://boxmarkcrm.bitrix24.com/telephony/detail.php")
    time.sleep(5)

    total_leads = {}  # Utiliza un diccionario en lugar de una lista

    lista_empresas = {
        "FB Secreto Azteca": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "FB Virgen Morena": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "FB Indio Amazónico": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "FB Maestros Esp": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "FB Botanica del Amor": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "FB Amarres Chicago": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "Google Secreto Azteca": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "Google Virgen Morena": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "Google Botanica del Amor": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "Google Amarres Chicago": "19:483ae87960d34b53b17a13738d1a6e8b@thread.skype",
        "Google Quick Comercial": "19:883d741dd2e545329a8ade55fe9e2b62@thread.skype",
        "Google Quick Residencial": "19:883d741dd2e545329a8ade55fe9e2b62@thread.skype",
        "Google Elite Spa Grasa": "19:99a5e08251374ee085d62b586667da96@thread.skype",
        "Google Elite Facial": "19:99a5e08251374ee085d62b586667da96@thread.skype",
    }

    empresas = list(lista_empresas.keys())


    for empresa in empresas:
        try:

            if empresa in lista_empresas:

                idChat = lista_empresas[empresa]

                contact = slogin.chats[idChat]

                inputFilter = driver.find_element(By.ID, 'voximplant_statistic_detail_filter_search')
                inputFilter.click()
                time.sleep(2)

                for i in range(5):
                    inputFilter = driver.find_element(By.NAME, 'PORTAL_USER_ID_label')
                    inputFilter.clear()  # Utiliza .clear() para borrar el campo de búsqueda
                    inputFilter.send_keys(empresa)
                    time.sleep(3)
                
                    try:
                        btn = driver.find_element(By.XPATH, f'(//div[contains(text(),"{empresa}")])[{i}]')
                        btn.click()
                    except:
                        print("Error al dar clic")

                buttonSearch = driver.find_element(By.CSS_SELECTOR,"button.ui-btn.ui-btn-primary.ui-btn-icon-search.main-ui-filter-field-button.main-ui-filter-find")
                buttonSearch.send_keys(Keys.ENTER)
                time.sleep(5)

                try:

                    fila_dict = {}

                    llamadaDesconocida = True
                    iteradorLlamada = 1

                    while llamadaDesconocida:

                        segundo_elemento = driver.find_element(By.XPATH, f'//tr[@class="main-grid-row main-grid-row-body"][{iteradorLlamada}]')
                        elementos_de_fila = segundo_elemento.find_elements(By.TAG_NAME, "td")

                        for i, elemento in enumerate(elementos_de_fila):
                            clave = f"columna_{i}"
                            valor = elemento.text
                            fila_dict[clave] = valor

                        claves_deseadas = ["columna_2", "columna_4", "columna_7", "columna_8"]
                        datos_filtrados = {clave: fila_dict[clave] for clave in claves_deseadas}

                        #Impresion de los elementos

                        consulta = f'SELECT * FROM leads WHERE call_date = "{datos_filtrados["columna_7"]}" AND  employee = "{datos_filtrados["columna_2"]}" '
                        cursor.execute(consulta)

                        resultados = cursor.fetchall()
                        print(resultados)
                        
                        if resultados == []:

                            try:
                                cursor.execute("INSERT INTO leads (employee, phone, call_date, status, day) VALUES (?, ?, ?, ?, ?)",(datos_filtrados["columna_2"], datos_filtrados["columna_4"], datos_filtrados["columna_7"], datos_filtrados["columna_8"],fecha_formateada))
                                print("SE INSERTA EN BASE DE DATOS ",empresa)

                                mensaje = f'Campaña "{datos_filtrados["columna_2"]}"\nNumero Lead "{datos_filtrados["columna_4"]}"\nFecha "{datos_filtrados["columna_7"]}"\nStatus "{datos_filtrados["columna_8"]}"'

                                contact.sendMsg(mensaje)

                            except:
                                print('ERROR AL INSERTAR DATOS EN DB')
                        #    
                            
                        else:
                            contact.sendMsg(f'NO HAY REGISTROS NUEVOS EN LA CAMPAÑA: {empresa}')
                            llamadaDesconocida = False

                        iteradorLlamada += 1
                except:
                    mensaje = f'No se encontraron registros para la empresa: {empresa}'
                    contact.sendMsg(mensaje)

        except Exception as e:
            print( "error en la iteración:", e)


    conexion.commit()
    conexion.close()


    driver.quit()

    time.sleep(intervalo_minutos * 60)
