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
# Desativar o gerenciador de senhas e a oferta de salvar senhas

options = Options()
prefs = {
    "credentials_enable_service": False,  # Desativa o serviço de credenciais
    "profile.password_manager_enabled": False  # Desativa o gerenciador de senhas
}
options.add_experimental_option("prefs", prefs)
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

def clicar_TAB(driver, tab_count=0): #Qtde de TABS
    for _ in range(tab_count):
        driver.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(2)    

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
            # cv2.imwrite("imagem_detectada.png", screen_image)
            # print("Imagem detectada salva como 'imagem_detectada.png'")

            if max_val >= 0.95:  # Ajuste de precisão para aceitar imagens com 98% de correspondência
                template_h, template_w = template_gray.shape[:2]
                click_x = max_loc[0] + template_w // 2
                click_y = max_loc[1] + template_h // 2

                cv2.rectangle(screen_image, (max_loc[0], max_loc[1]), 
                              (max_loc[0] + template_w, max_loc[1] + template_h), 
                              (0, 255, 0), 2)
                # cv2.imwrite("clicado.png", screen_image)
                # print("Print da área clicada salvo como 'clicado.png'.")

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

def Clique_Ousado_Scroll(driver, imagem_alvo, timeout=30, scroll_step=300):  
    try:
        if not os.path.exists(imagem_alvo):
            print(f"Imagem alvo não encontrada: {imagem_alvo}")
            return
        
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        tempo_espera = 0
        intervalo = 2
        scroll_attempts = 5  # Quantidade de tentativas de rolagem antes de desistir

        while tempo_espera < timeout:
            for _ in range(scroll_attempts):
                driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_step)
                time.sleep(1)

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

                if max_val >= 0.95:  
                    template_h, template_w = template_gray.shape[:2]
                    click_x = max_loc[0] + template_w // 2
                    click_y = max_loc[1] + template_h // 2

                    scroll_x, scroll_y = driver.execute_script("return [window.scrollX, window.scrollY];")

                    # Ajuste para rolagem e posição real
                    page_x = click_x + scroll_x
                    page_y = click_y + scroll_y

                    print(f"Clicando exatamente em X: {page_x}, Y: {page_y} (Scroll X: {scroll_x}, Y: {scroll_y})")

                    # Rolar até o ponto do clique para garantir visibilidade
                    driver.execute_script(f"window.scrollTo({page_x - 50}, {page_y - 50});")
                    time.sleep(1)

                    # Clique real usando JavaScript
                    driver.execute_script(f"document.elementFromPoint({click_x}, {click_y}).click();")
                    return  

            print("Imagem não encontrada após rolar, tentando novamente...")
            tempo_espera += intervalo
            time.sleep(intervalo)
        
        print("Imagem não encontrada após tempo limite.")
    except Exception as e:
        print(f"Erro ao detectar ou clicar na imagem: {e}")


diretorio_base = r'C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Baixa Credenciados'

imagem_ok = os.path.join(diretorio_base, 'ok.png')
imagem_totvs_inicio = os.path.join(diretorio_base, 'totvs_inicio.png')
imagem_nome = os.path.join(diretorio_base, 'nome.png')
imagem_favorito = os.path.join(diretorio_base, 'favorito.png')
imagem_funcoes_cpg = os.path.join(diretorio_base, 'funcoes_cpg.png')
imagem_confirmar = os.path.join(diretorio_base, 'confirmar.png')
imagem_outrasacoes = os.path.join(diretorio_base, 'outras_acoes.png')
imagem_bordero = os.path.join(diretorio_base, 'bordero.png')
imagem_bordero2 = os.path.join(diretorio_base, 'bordero2.png')
imagem_clicado2 = os.path.join(diretorio_base, 'clicado2.png')
imagem_banco = os.path.join(diretorio_base, 'banco.png')
imagem_ok2 = os.path.join(diretorio_base, 'ok2.png')
imagem_filial_vlrtitulo = os.path.join(diretorio_base, 'filial_vlrtitulo.png')

# Abrir página
navegador.get("http://an148124.protheus.cloudtotvs.com.br:1703/webapp/")
WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
actions = ActionChains(navegador)

detectar_e_clicar_imagem(navegador, imagem_ok)
time.sleep(10)

esperar_imagem_aparecer(navegador, imagem_totvs_inicio)
time.sleep(3)

digitar_entrada_com_TAB(navegador, os.getenv("LOGIN"), 1)
digitar_entrada_com_TAB(navegador, os.getenv("SENHA"), 1)
actions.send_keys(Keys.ENTER).perform()
time.sleep(10)

esperar_imagem_aparecer(navegador, imagem_nome)
time.sleep(3)

for _ in range(2):
    actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
    time.sleep(0.5)

time.sleep(2)

digitar_entrada_com_TAB(navegador, "12/03/2025",2)
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


digitar_entrada_com_TAB(navegador, "6",5)
actions.send_keys(Keys.ENTER).perform()
time.sleep(10)

Clique_Ousado(navegador, imagem_favorito)
time.sleep(5)

Clique_Ousado(navegador, imagem_funcoes_cpg)
time.sleep(5)

Clique_Ousado(navegador, imagem_confirmar)
time.sleep(15)

Clique_Ousado(navegador, imagem_outrasacoes)
time.sleep(2)

Clique_Ousado(navegador, imagem_bordero)
time.sleep(2)

Clique_Ousado(navegador, imagem_bordero2)
time.sleep(2)

clicar_TAB(navegador, 7)
time.sleep(2)


digitar_entrada_com_TAB(navegador, "756",1)
time.sleep(1)
digitar_entrada_com_TAB(navegador, "3337",1)
time.sleep(1)
digitar_entrada_com_TAB(navegador, "3780624",8)
time.sleep(1)
digitar_entrada_com_TAB(navegador,"02",1)
time.sleep(1)
digitar_entrada_com_TAB(navegador,"20",1)
time.sleep(1)
Clique_Ousado(navegador, imagem_ok2)
time.sleep(3)

Clique_Ousado_Scroll(navegador, imagem_filial_vlrtitulo)


# Chamar função após o clique
navegador.quit()
