import os
import requests
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
id_value = os.getenv("ID")

url = f"https://script.google.com/a/macros/angelscapital.com.br/s/{id_value}/exec"
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

time.sleep(15)



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
        print(f"célula {cell}")
    else:
        print(f"Erro ao escrever na célula {cell}: {response.status_code} - {response.text}")

last_processed_row = 2  # Inicializando na linha 2, onde começa a busca

while True:

    rows_processed = 0  # Contador de transferências processadas
    rows_to_process = []  # Lista para armazenar as linhas com status "PROCESSANDO"
    


    for row in range(last_processed_row, 1000):
        cell_a = f"A{row}"
        value_a = ler_celula(cell_a)

        if not value_a or value_a.strip() == "":
            print("Fim da planilha. Encerrando...")
            exit()

        cell_h = f"H{row}"
        value_h = ler_celula(cell_h)

        if value_h.strip().upper() == "PROCESSANDO":
            rows_to_process.append(row)  # Adicionar a linha à lista de transferências a serem processadas

        if len(rows_to_process) >= 3:  # Se encontrou 3 linhas "PROCESSANDO", interrompe a busca
            break

    if len(rows_to_process) == 0:
        print("Nenhuma transferência com status 'PROCESSANDO' encontrada. Encerrando...")
        break
    

    for row in rows_to_process:

        cell_a = f"A{row}"
        value_a = ler_celula(cell_a)

        cell_h = f"H{row}"
        value_h = ler_celula(cell_h)

        cell_b = f"B{row}"
        value_b = ler_celula(cell_b)

        cell_f = f"f{row}"
        value_f = ler_celula(cell_f)


        try:
            #CAPTURAR NOME PAINELFOMENTO
            xpathnome = f"//td[@class='text-left' and contains(text(), '{value_a}')]"
            nome_td = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpathnome)))
            nome = nome_td.text

            #CAPTURAR NÚMERO CARTAO
            tdnumerocartao = f"//td[@class='text-left' and contains(text(), '{value_a}')]/following-sibling::td[contains(text(), '{value_b}')]"
            td_centro = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, tdnumerocartao)))
            numero_td = td_centro.text

            #CAPTURAR O FAVORECIDO
            xpath_td_nome = f"//td[@class='text-center' and contains(text(), '{value_f}')]"
            td_nome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_td_nome)))
            favorecido = td_nome.text



            #CAPTURAR BOTÃO DE SELECIONAR
            botaoselecionar = xpathnome + "/preceding-sibling::td[1]//div[contains(@class, 'q-toggle')]"
            botao1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, botaoselecionar)))
            #CLICAR NO BOTÃO
            actions = ActionChains(driver)
            actions.move_to_element(botao1).click().perform()

            print(f"Nome capturado na linha {row}: {nome}, Número capturado: {numero_td}, Favorecido capturado: {favorecido}")

            cell_h = f"H{row}"
            escrever_celula(cell_h, "LIBERADO")

            print("Nome capturado:", nome)
        except Exception as e:
            print(f"Erro ao buscar o nome na linha {row}: {str(e)}")

    
    last_processed_row = rows_to_process[-1] + 1  # A última linha processada + 1


    #Esperar para clicar em "Enviar Transferências Selecionadas"
    time.sleep(3)


    try:
        #ENVIAR TRANSFERÊNCIAS SELECIONADAS
        botaotransferencias = "//span[contains(@class, 'q-btn__content') and span[text()='Enviar Transferências Selecionadas']]"
        botao2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, botaotransferencias)))
        #CLICAR NO BOTÃO
        actions = ActionChains(driver)
        actions.move_to_element(botao2).click().perform()
        print("Botão 'Enviar Transferências Selecionadas' clicado com sucesso!")


        time.sleep(2)


        #ENVIAR
        botao_enviar = "//span[@class='block' and text()='Enviar']"
        botao3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, botao_enviar)))
        #CLICAR NO BOTÃO
        actions = ActionChains(driver)
        actions.move_to_element(botao3).click().perform()

    except Exception as e:
            print(f"Erro ao clicar no botão de transferências: {str(e)}")


    time.sleep(15)


