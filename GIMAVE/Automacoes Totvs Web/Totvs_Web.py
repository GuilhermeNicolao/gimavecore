from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import cv2
import os 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
from dotenv import load_dotenv

# Configurar opções do Chrome
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

load_dotenv()

# Inicializar navegador
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

def digitar_entrada_com_TAB(driver, texto, tab_count=0): #Qtde de TABS
    driver.switch_to.active_element.send_keys(texto)
    for _ in range(tab_count):
        driver.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(1)

def digitar_entrada(driver, texto, tab_count=0): #Inserir textos
    driver.switch_to.active_element.send_keys(texto)
    time.sleep(1)

def esperar_imagem_aparecer(driver, imagem_alvo, timeout=30): #Espera a imagem aparecer
    try:
        if not os.path.exists(imagem_alvo):
            raise FileNotFoundError(f"Imagem alvo não encontrada: {imagem_alvo}")

        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        tempo_espera = 0
        intervalo = 2
        while tempo_espera < timeout:
            screenshot = driver.get_screenshot_as_png()
            screen_array = np.frombuffer(screenshot, dtype=np.uint8)
            screen_image = cv2.imdecode(screen_array, cv2.IMREAD_COLOR)
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

            template = cv2.imread(imagem_alvo, cv2.IMREAD_COLOR)
            if template is None:
                raise ValueError(f"Erro ao carregar a imagem do template: {imagem_alvo}")

            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7  # Reduzido para melhorar detecção
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                print(f"Imagem encontrada: {imagem_alvo}")
                return True
            else:
                print("Imagem ainda não visível, aguardando...")
                time.sleep(intervalo)
                tempo_espera += intervalo
        
        print("Imagem não encontrada após tempo limite.")
        return False
    except Exception as e:
        print(f"Erro ao detectar a imagem: {e}")
        return False

def detectar_e_clicar_imagem(driver, imagem_alvo, timeout=30): #Clicar de fato no botão
    try:
        if not os.path.exists(imagem_alvo):
            raise FileNotFoundError(f"Imagem alvo não encontrada: {imagem_alvo}")

        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        tempo_espera = 0
        intervalo = 2
        while tempo_espera < timeout:
            screenshot = driver.get_screenshot_as_png()
            screen_array = np.frombuffer(screenshot, dtype=np.uint8)
            screen_image = cv2.imdecode(screen_array, cv2.IMREAD_COLOR)
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

            template = cv2.imread(imagem_alvo, cv2.IMREAD_COLOR)
            if template is None:
                raise ValueError(f"Erro ao carregar a imagem do template: {imagem_alvo}")

            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7  # Reduzido para melhorar detecção
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                template_h, template_w = template_gray.shape[:2]
                click_x = max_loc[0] + template_w // 2
                click_y = max_loc[1] + template_h // 2

                screen_width = driver.execute_script("return window.innerWidth;")
                screen_height = driver.execute_script("return window.innerHeight;")
                
                click_x = min(max(click_x, 0), screen_width - 1)
                click_y = min(max(click_y, 0), screen_height - 1)
                
                print(f"Tentando clicar em X: {click_x}, Y: {click_y}, Tela: {screen_width}x{screen_height}")
                time.sleep(1)
                webdriver.ActionChains(driver).move_by_offset(click_x, click_y).click().perform()
                return
            else:
                print("Imagem ainda não visível, aguardando...")
                time.sleep(intervalo)
                tempo_espera += intervalo
        
        print("Imagem não encontrada após tempo limite.")
    except Exception as e:
        print(f"Erro ao detectar ou clicar na imagem: {e}")

def Clique_Ousado(driver, imagem_alvo, timeout=30): #Reconhece a imagem e clica nela (independente de ser um botão ou não)
    try:
        if not os.path.exists(imagem_alvo):
            print(f"Imagem alvo não encontrada: {imagem_alvo}")
            return
        
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        tempo_espera = 0
        intervalo = 2
        while tempo_espera < timeout:
            screenshot = driver.get_screenshot_as_png()
            screen_array = np.frombuffer(screenshot, dtype=np.uint8)
            screen_image = cv2.imdecode(screen_array, cv2.IMREAD_COLOR)
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

            template = cv2.imread(imagem_alvo, cv2.IMREAD_COLOR)
            if template is None:
                print(f"Erro ao carregar a imagem do template: {imagem_alvo}")
                return
            
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            print(f"Precisão da imagem encontrada: {max_val:.2f}")

            # Salvar a imagem detectada para análise
            cv2.imwrite("imagem_detectada.png", screen_image)
            print("Imagem detectada salva como 'imagem_detectada.png'")

            if max_val >= 0.95:  # Ajuste de precisão para aceitar imagens com 98% de correspondência
                template_h, template_w = template_gray.shape[:2]
                click_x = max_loc[0] + template_w // 2
                click_y = max_loc[1] + template_h // 2

                cv2.rectangle(screen_image, (max_loc[0], max_loc[1]), 
                              (max_loc[0] + template_w, max_loc[1] + template_h), 
                              (0, 255, 0), 2)
                cv2.imwrite("clicado.png", screen_image)
                print("Print da área clicada salvo como 'clicado.png'.")

                scroll_x, scroll_y = driver.execute_script("return [window.scrollX, window.scrollY];")

                # Posição real do clique considerando a rolagem
                page_x = click_x + scroll_x
                page_y = click_y + scroll_y

                print(f"Clicando exatamente em X: {page_x}, Y: {page_y} (Considerando scroll X: {scroll_x}, Y: {scroll_y})")

                # Rolagem até a posição do clique para garantir visibilidade
                driver.execute_script(f"window.scrollTo({page_x - 50}, {page_y - 50});")
                time.sleep(1)

                # Simulação de clique real no ponto exato
                driver.execute_script(f"document.elementFromPoint({click_x}, {click_y}).click();")
                return  
            
            print("Imagem não encontrada com 95% de precisão, aguardando...")
            time.sleep(intervalo)
            tempo_espera += intervalo
        
        print("Imagem não encontrada após tempo limite.")
    except Exception as e:
        print(f"Erro ao detectar ou clicar na imagem: {e}")


# Abrir página
navegador.get("http://an148124.protheus.cloudtotvs.com.br:1703/webapp/")
WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
actions = ActionChains(navegador)

imagem_alvo = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Teste Totvs Web\ok.png'
detectar_e_clicar_imagem(navegador, imagem_alvo)
time.sleep(10)

imagem_alvo = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Teste Totvs Web\totvs_inicio.png'
esperar_imagem_aparecer(navegador, imagem_alvo)
time.sleep(3)

digitar_entrada_com_TAB(navegador, os.getenv("LOGIN"), 1)
digitar_entrada_com_TAB(navegador, os.getenv("SENHA"), 1)
actions.send_keys(Keys.ENTER).perform()
time.sleep(10)

imagem_alvo = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Teste Totvs Web\nome.png'
esperar_imagem_aparecer(navegador, imagem_alvo)
time.sleep(3)

for _ in range(2):
    actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
    time.sleep(0.5)

time.sleep(2)

digitar_entrada_com_TAB(navegador, "17/03/2025",2)
time.sleep(0.5)
actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
nome_digitado = pyperclip.paste()
print(nome_digitado)

if nome_digitado == '06':
    digitar_entrada(navegador, "06")
    for _ in range(4):
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
else:
    digitar_entrada(navegador, "06")
    for _ in range(3):
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)


digitar_entrada_com_TAB(navegador, "5",5)
actions.send_keys(Keys.ENTER).perform()
time.sleep(10)

imagem_alvo = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Teste Totvs Web\favorito.png'
Clique_Ousado(navegador, imagem_alvo)
time.sleep(5)

imagem_alvo = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Teste Totvs Web\pedidos_venda.png'
Clique_Ousado(navegador, imagem_alvo)
time.sleep(5)

imagem_alvo = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Teste Totvs Web\esperar_data.png'
esperar_imagem_aparecer(navegador, imagem_alvo)
time.sleep(1)
digitar_entrada(navegador, "13/03/2025")
time.sleep(2)

actions.send_keys(Keys.ENTER).perform()
time.sleep(2)

imagem_alvo = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Teste Totvs Web\esperar_nat.png'
esperar_imagem_aparecer(navegador, imagem_alvo)
time.sleep(1)
digitar_entrada(navegador, "2152101005")
time.sleep(2)

actions.send_keys(Keys.ENTER).perform()
time.sleep(10)


# Chamar função após o clique
navegador.quit()
