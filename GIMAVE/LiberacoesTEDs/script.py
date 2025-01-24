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

# url = "https://script.google.com/macros/s//exec"
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



while True:
    pass