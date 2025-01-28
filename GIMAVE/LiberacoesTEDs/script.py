import os
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

load_dotenv()

url = "https://script.google.com/a/macros/angelscapital.com.br/s/AKfycbyxvZBaE5Ug0jmBCAZ_ym7NdSWwO5Q3AcIPPScGt5TfdYCUJsSW_VMt_RUDQqiHoM_Ang/exec"
driver = webdriver.Chrome()
driver.get("https://fomento.eucard.com.br/transferencias")
time.sleep(3)  

#LOGIN
cpf_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='CPF *']")))
cpf_field.click() 
cpf_field.send_keys(os.getenv("CPF"))  

#SENHA
senha_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Senha *']")))
senha_field.click() 
senha_field.send_keys(os.getenv("SENHA"))

time.sleep(2)

#ENTRAR
entrar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.q-btn__content.text-center")))
entrar_button.click()

time.sleep(2)



#ABRIR MENU
menu_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='q-icon notranslate material-icons' and @aria-hidden='true']")))
menu_icon.click()

time.sleep(1)

#CLICAR NO "EUCARD"
eucard_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'q-item') and contains(., 'Eucard')]")))
eucard_button.click()

time.sleep(1)

#CLICAR NO "TRANSFERÊNCIAS"
transferencias_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/transferencias' and contains(@class, 'menu__item')]")))
transferencias_link.click()

time.sleep(10)



def ler_celula(cell):
    params = {"action": "read", "cell": cell}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("value", None)
    else:
        print(f"Erro ao ler a célula {cell}: {response.status_code} - {response.text}")
        return None


def escrever_celula(cell, value):
    params = {"action": "write", "cell": cell, "value": value}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"{value}' célula {cell}")
    else:
        print(f"Erro ao escrever na célula {cell}: {response.status_code} - {response.text}")


row = 97

for i in range(3):

    cell_a = f"A{row}"
    value_a = ler_celula(cell_a)

    try:
        #CAPTURAR NOME PAINELFOMENTO
        xpath_dinamico = f"//td[@class='text-left' and contains(text(), '{value_a}')]"
        nome_td = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_dinamico)))
        nome = nome_td.text

        #pressionar_botao = nome_td.find_element(By.XPATH, "./preceding-sibling::td//div[@class='q-toggle__track']")
        #pressionar_botao.click()

        print("Nome capturado:", nome)
    except Exception as e:
        print(f"Erro ao buscar o nome na linha {row}: {str(e)}")

    row +=1

while True:
    pass