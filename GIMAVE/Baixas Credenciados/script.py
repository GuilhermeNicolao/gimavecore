import os
import pyautogui
import requests
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://an148124.protheus.cloudtotvs.com.br:1703/webapp/")

time.sleep(33) #timesleep30 a timesleep35

# Campo "Atualizações"
atualizacoes_element = WebDriverWait(driver, 20).until(
EC.element_to_be_clickable((By.XPATH, "//span[@title='Atualizações (19)']//u[text()='tualizações (19)']")))
atualizacoes_element.click()

time.sleep(10)
