from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import timedelta
import time
import numpy as np
import cv2
import os 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import matplotlib.pyplot as plt
import pandas as pd
from selenium.common.exceptions import TimeoutException



# Configurar opções do Chrome
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Executar em modo headless
# options.add_argument("--headless=new")

# Desativar o gerenciador de senhas e a oferta de salvar senhas
prefs = {
    "credentials_enable_service": False,  # Desativa o serviço de credenciais
    "profile.password_manager_enabled": False  # Desativa o gerenciador de senhas
}
options.add_experimental_option("prefs", prefs)

# Inicializar navegador com as opções
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

def apagar_Campo(driver, elemento_id, tempo_espera=30):
    """
    Espera até que o elemento identificado pelo ID seja clicável, clica, limpa o campo e define "0,00".

    :param driver: Instância do WebDriver.
    :param elemento_id: ID do elemento a ser manipulado.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    """
    try:
        elemento = WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.ID, elemento_id))
        )
        driver.execute_script(f"document.getElementById('{elemento_id}').click();")
        print("Elemento clicado com sucesso.")

        # Limpando o campo via JavaScript
        driver.execute_script(f"document.getElementById('{elemento_id}').value = '';")
        print("Campo limpo com sucesso.")

        # Definindo o valor como "0,00"
        driver.execute_script(f"document.getElementById('{elemento_id}').value = '0,00';")
        print('Valor "0,00" definido com sucesso.')
    except Exception as e:
        print(f"Erro ao clicar, limpar ou definir o valor do elemento: {e}")

def digitar_entrada_com_TAB(driver, texto, tab_count=0):
    driver.switch_to.active_element.send_keys(texto)
    for _ in range(tab_count):
        driver.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(1)

def esperar_e_clicar_simples(driver, elemento_id, tempo_espera=30):
    """
    Espera até que o elemento identificado pelo ID seja clicável e, então, realiza um duplo clique.

    :param driver: Instância do WebDriver.
    :param elemento_id: ID do elemento a ser clicado.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    """
    try:
        # Espera até que o elemento seja clicável
        WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.ID, elemento_id))
        )

        # Localiza o elemento pelo ID
        elemento = driver.find_element(By.ID, elemento_id)

        # Realiza o duplo clique usando ActionChains
        action = ActionChains(driver)
        action.double_click(elemento).perform()  # Duplo clique
        print('Duplo clique realizado com sucesso.')
    except Exception as e:
        print(f"Erro ao realizar o duplo clique: {e}")

def digitar_entrada(driver, texto, tab_count=0):
    driver.switch_to.active_element.send_keys(texto)
    time.sleep(1)

def esperar_imagem_aparecer(driver, imagem_alvo, timeout=80):
    try:
        if not os.path.exists(imagem_alvo):
            raise FileNotFoundError(f"Imagem alvo não encontrada: {imagem_alvo}")
        
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        tempo_espera = 0
        intervalo = 2
        
        while True:
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
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                print(f"Imagem encontrada: {imagem_alvo}")
                return True
            else:
                print("Imagem ainda não visível, aguardando...")
                time.sleep(intervalo)
                tempo_espera += intervalo
                
                if tempo_espera >= timeout:
                    print("Tempo limite atingido. Imagem não encontrada.")
                    return False
    except Exception as e:
        print(f"Erro ao detectar a imagem: {e}")
        return False

def detectar_e_clicar_imagem(driver, imagem_alvo, timeout=80):
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

def Clique_Ousado(driver, imagem_alvo, timeout=80):
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

            if max_val >= 0.90:  # Ajuste de precisão para aceitar imagens com 98% de correspondência
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
            
            print("Imagem não encontrada com 90% de precisão, aguardando...")
            time.sleep(intervalo)
            tempo_espera += intervalo
        
        print("Imagem não encontrada após tempo limite.")
    except Exception as e:
        print(f"Erro ao detectar ou clicar na imagem: {e}")

def Clique_Ousado_Duas_Vezes(driver, imagem_alvo, timeout=80):
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

            if max_val >= 0.90:  # Ajuste de precisão para aceitar imagens com 90% de correspondência
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

                # Criando a ação de duplo clique com Selenium
                elemento = driver.execute_script(f"return document.elementFromPoint({click_x}, {click_y});")
                if elemento:
                    action = ActionChains(driver)
                    action.move_to_element(elemento).double_click().perform()
                    print("Duplo clique realizado!")
                    return
                else:
                    print("Elemento não encontrado para clique.")

            print("Imagem não encontrada com 90% de precisão, aguardando...")
            time.sleep(intervalo)
            tempo_espera += intervalo
        
        print("Imagem não encontrada após tempo limite.")
    except Exception as e:
        print(f"Erro ao detectar ou clicar na imagem: {e}")

def fatura (driver, imagem_alvo, tempo_maximo=3, confidence=0.7):
    """
    Verifica se o pedido está faturado em segundo plano sem interações diretas.

    :param driver: Instância do WebDriver do Selenium.
    :param imagem_alvo: Caminho para a imagem de referência.
    :param tempo_maximo: Tempo máximo de espera para encontrar a imagem.
    :param confidence: Precisão mínima para considerar a imagem como encontrada.
    :return: True se a imagem for encontrada, False caso contrário.
    """
    if not os.path.exists(imagem_alvo):
        print(f"Imagem alvo não encontrada: {imagem_alvo}")
        return False

    # Esperar a página carregar completamente
    WebDriverWait(driver, tempo_maximo).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    inicio = time.time()
    intervalo = 0.5  # Intervalo entre verificações
    template = cv2.imread(imagem_alvo, cv2.IMREAD_COLOR)
    
    if template is None:
        print(f"Erro ao carregar a imagem de referência: {imagem_alvo}")
        return False
    
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    while time.time() - inicio < tempo_maximo:
        # Capturar tela do navegador
        screenshot = driver.get_screenshot_as_png()
        screen_array = np.frombuffer(screenshot, dtype=np.uint8)
        screen_image = cv2.imdecode(screen_array, cv2.IMREAD_COLOR)
        screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

        # Comparação da imagem
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        print(f"Precisão da imagem detectada: {max_val:.2f}")

        if max_val >= confidence:  # Se atingir a confiança esperada
            print("Imagem encontrada!")
            return True

        time.sleep(intervalo)

    print("Imagem não encontrada dentro do tempo máximo.")
    return False

def esperar_e_clicar(driver, elemento_id, tempo_espera=30, cliques=2):
    """
    Espera até que o elemento identificado pelo ID esteja presente e realiza múltiplos cliques.

    :param driver: Instância do WebDriver.
    :param elemento_id: ID do elemento a ser clicado.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    :param cliques: Número de cliques a serem realizados (padrão: 2 - duplo clique).
    """
    try:
        # Espera até que o elemento esteja presente no DOM
        elemento = WebDriverWait(driver, tempo_espera).until(
            EC.presence_of_element_located((By.ID, elemento_id))
        )

        # Espera até que o elemento esteja visível e clicável
        WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.ID, elemento_id))
        )

        # Executa os cliques necessários
        action = ActionChains(driver)
        for _ in range(cliques):
            action.click(elemento)
        action.perform()
        
        print(f'{cliques} clique(s) realizado(s) com sucesso.')
    except Exception as e:
        print(f"Erro ao clicar no elemento '{elemento_id}': {e}")

def inserir_Sem_Espaço(driver, elemento_id, texto, tempo_espera=30):
    """
    Espera até que o elemento identificado pelo ID seja clicável, limpa o campo e insere o texto.
    Se falhar, insere o texto forçadamente via JavaScript.
    Garante que não haverá espaços extras após a inserção.

    :param driver: Instância do WebDriver.
    :param elemento_id: ID do elemento onde o texto será inserido.
    :param texto: Texto a ser inserido no elemento.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    """
    texto = texto.strip()  # Remover qualquer espaço em branco no início e no final do texto
    
    try:
        # Espera até o elemento ficar clicável
        elemento = WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.ID, elemento_id))
        )
        
        # Limpar o campo completamente com JavaScript
        driver.execute_script(f"document.getElementById('{elemento_id}').value = '';")
        print(f"Campo {elemento_id} limpo com sucesso.")

        # Agora, insira o texto sem espaços extras
        driver.execute_script(f"document.getElementById('{elemento_id}').value = '{texto}';")
        
        # Garantir que o foco está no campo para a inserção funcionar corretamente
        driver.execute_script(f"document.getElementById('{elemento_id}').focus();")
        
        print(f"Texto '{texto}' inserido com sucesso via JavaScript no elemento {elemento_id}.")
    except Exception as e:
        print(f"Erro ao inserir texto no elemento {elemento_id}: {e}")

        print(f"Erro ao inserir texto no elemento {elemento_id}: {e}")

def inserir_Com_Python(driver, elemento_id, texto, tempo_espera=30):
    texto = str(texto).strip()  # Converter para string antes de strip()

    try:
        elemento = WebDriverWait(driver, tempo_espera).until(
            EC.presence_of_element_located((By.ID, elemento_id))
        )

        # Verificar se o elemento está habilitado e visível
        if not elemento.is_enabled():
            print(f"O elemento {elemento_id} está desabilitado.")
            return
        if not elemento.is_displayed():
            print(f"O elemento {elemento_id} está oculto.")
            return

        elemento.click()  # Clicar para garantir que está ativo
        time.sleep(0.5)  # Pequeno delay para evitar erros

        elemento.send_keys(Keys.CONTROL + "a")  # Selecionar todo o texto
        elemento.send_keys(Keys.BACKSPACE)  # Apagar texto anterior
        time.sleep(0.5)  

        # Inserir o texto caractere por caractere
        for char in texto:
            elemento.send_keys(char)
            time.sleep(0.1)  # Pequeno delay entre caracteres

        print(f"Texto '{texto}' inserido com sucesso no elemento {elemento_id}.")
    
    except TimeoutException:
        print(f"Erro: Tempo limite excedido ao tentar acessar o elemento {elemento_id}.")
    except Exception as e:
        print(f"Erro inesperado ao inserir texto no elemento {elemento_id}: {e}")
        # Tentar via JavaScript como fallback
        driver.execute_script(f"document.getElementById('{elemento_id}').value = '{texto}';")
        print(f"Texto inserido via JavaScript no elemento {elemento_id}.")


# Abrir página
navegador.get("http://an148124.protheus.cloudtotvs.com.br:1703/webapp/")
WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
actions = ActionChains(navegador)

imagem_alvo = 'ok.png'
detectar_e_clicar_imagem(navegador, imagem_alvo)
time.sleep(5)

imagem_alvo = 'totvs_inicio.png'
esperar_imagem_aparecer(navegador, imagem_alvo)
time.sleep(3)

#Colocar loguin e senha
digitar_entrada_com_TAB(navegador, "GILBERTONETO", 1)
digitar_entrada_com_TAB(navegador, "G1mave@2025", 1)
actions.send_keys(Keys.ENTER).perform()
time.sleep(5)

imagem_alvo = 'nome.png'
esperar_imagem_aparecer(navegador, imagem_alvo)
time.sleep(1)

for _ in range(2):
    actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
    time.sleep(0.5)
time.sleep(1)


# Processar cada linha da tabela
# Caminho do arquivo
caminho_arquivo = r"C:\Users\Gilberto.Neto\Desktop\Baixas TOTVS\Base_Dados.xlsx"

# Carregar a planilha
try:
    tabela_produtos = pd.read_excel(caminho_arquivo, dtype=str, engine="openpyxl")
except Exception as e:
    print(f"❌ Erro ao carregar a planilha: {e}")
    exit()

# Remover espaços extras dos nomes das colunas
tabela_produtos.columns = tabela_produtos.columns.str.strip()

# Verificar se "Dt Baixa" está presente
if "Dt Baixa" not in tabela_produtos.columns:
    print("⚠️ A coluna 'Dt Baixa' não foi encontrada. Tentando na segunda linha...")

    try:
        tabela_produtos = pd.read_excel(caminho_arquivo, header=1, dtype=str, engine="openpyxl")
        tabela_produtos.columns = tabela_produtos.columns.str.strip()

        if "Dt Baixa" in tabela_produtos.columns:
            print("✅ A coluna 'Dt Baixa' foi encontrada na segunda linha.")
        else:
            print("❌ A coluna 'Dt Baixa' NÃO foi encontrada. Verifique o arquivo.")
            exit()

    except Exception as e:
        print(f"❌ Erro ao recarregar a planilha: {e}")
        exit()
else:
    print("✅ A coluna 'Dt Baixa' foi encontrada corretamente na primeira linha.")

# Mostrar as primeiras linhas para depuração
print(tabela_produtos.head())

# Obter a primeira data válida da coluna "Dt Baixa"
datas_validas = tabela_produtos["Dt Baixa"].dropna()  # Remove valores NaN
if datas_validas.empty:
    print("❌ Nenhuma data válida encontrada na coluna 'Dt Baixa'.")
    exit()

# Tentar converter a primeira data válida
primeira_data = pd.to_datetime(datas_validas.iloc[0], errors='coerce')

# Verificar se a conversão foi bem-sucedida
if pd.isna(primeira_data):
    print("❌ Erro: Data inválida ou não encontrada.")
    exit()
else:
    data_formatada = primeira_data.strftime('%d/%m/%Y')
    print("✅ Data formatada:", data_formatada)

# Chamar a função para digitar os dados no Selenium
digitar_entrada_com_TAB(navegador, data_formatada, 2)
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

#Colocar Modulo
digitar_entrada_com_TAB(navegador, "6",5)
actions.send_keys(Keys.ENTER).perform()
time.sleep(5)

# Clicar em Favorito
imagem_alvo = 'favorito.png'
Clique_Ousado(navegador, imagem_alvo)
time.sleep(5)

#Contas a Receber 
imagem_alvo = 'baixas_Receber.png'
Clique_Ousado(navegador, imagem_alvo)
time.sleep(2)

try:
    elemento = WebDriverWait(navegador, 40).until(
        EC.presence_of_element_located((By.ID, "COMP4512"))
    )
    elemento.click()
    print("COMP4512 encontrado e clicado.")
except TimeoutException:
    print("COMP4512 não encontrado, seguindo com o código.")

#Esperar Filtro Aparecer
imagem_alvo = 'filtro.png'
esperar_imagem_aparecer(navegador, imagem_alvo)
time.sleep(1)

#CLICAR EM FILTRO
esperar_e_clicar(navegador, 'COMP4526')
time.sleep(1)

#Clicar em Pedido Filtro
esperar_e_clicar(navegador, 'COMP6025')
time.sleep(3)

#Clicar em saldo diferente de zero
esperar_e_clicar(navegador, 'COMP6017')
time.sleep(1)

#Clicar em Aplicar
esperar_e_clicar(navegador, 'COMP6048')
time.sleep(3)

# Inserir O valor: COMP9003
digitar_entrada_com_TAB(navegador ,"056589")
time.sleep (2)

#Clicar em avançar COMP9006
esperar_e_clicar(navegador, 'COMP9006')
time.sleep(5)

print(tabela_produtos.head())  # Mostra as primeiras linhas da tabela
print(f"Total de linhas: {len(tabela_produtos)}")  # Exibe o total de registros

# Processar cada linha da tabela
def processar_linha(linha):
    try:

        # Extraindo dados da linha
        Data_Baixa = pd.to_datetime(tabela_produtos.loc[linha, "Dt Baixa"])
        Pedido = tabela_produtos.loc[linha, "Pedido"]
        Fatura = tabela_produtos.loc[linha, "Fatura"]
        Value_Titulo = tabela_produtos.loc[linha, "Valor"]
        Hist = tabela_produtos.loc[linha, "Histórico"]

        # Campos para baixar
        Juros = tabela_produtos.loc[linha, "Juros"]
        Desconto = tabela_produtos.loc[linha, "Desconto"]
        Bank = "756"
        Agen = "3337"
        Cont = str(tabela_produtos.loc[linha, "Conta"])
        statuns = tabela_produtos.loc[linha, "statuns"]

        # Formatação de valores
        try:
            Value_Titulo = f"{float(Value_Titulo):.2f}".replace(".", ",")
        except ValueError:
            Value_Titulo = "0,00"
   
        try:
            Juros = f"{float(Juros):.2f}".replace(".", ",")
        except ValueError:
            Juros = "0,00"

        try:
            Desconto = f"{float(Desconto):.2f}".replace(".", ",")
        except ValueError:
            Desconto = "0,00"
        
        #Formatação De Datas
        data_formatada = Data_Baixa.strftime('%m/%d/%Y')
        Data_Baixa = data_formatada
        
        #CLICAR EM FILTRO
        esperar_e_clicar(navegador, 'COMP4526')
        time.sleep(3)

        #Aqui vai Tentar Clicar em aplicar se Der erro vai voltar e clicar no filtro antes 
        try:
            ##Esperara Baixass
            imagem_alvo = 'aplicar.png'
            esperar_imagem_aparecer(navegador, imagem_alvo)
            time.sleep(2)

            #Clicar em Aplicar
            esperar_e_clicar(navegador, 'COMP6048')
            time.sleep(1)

        except Exception as e:
            print(f"Erro ao clicar em 'não': {e}")
            
            try:
                #CLICAR EM FILTRO
                esperar_e_clicar(navegador, 'COMP4526')
                time.sleep(2)

                ##Esperara Baixass
                imagem_alvo = 'aplicar.png'
                esperar_imagem_aparecer(navegador, imagem_alvo)
                time.sleep(2)
                    
                #Clicar em Aplicar
                esperar_e_clicar(navegador, 'COMP6048')
                time.sleep(2)
            except Exception as e:
                print(f"Erro ao Esperar a tela de baixas: {e}")

        ##Esperara esperar_pedido
        imagem_alvo = 'esperar_pedido.png'
        esperar_imagem_aparecer(navegador, imagem_alvo)
        time.sleep(2)

        # Inserir O valor: PEDIDO
        inserir_Com_Python(navegador,"COMP9003" ,Pedido)
        time.sleep(2)

        #Clicar em avançar COMP9006
        esperar_e_clicar(navegador, "COMP9006")
        time.sleep(3)

        def formatar_moeda(valor):
            """
            Converte um número para o formato de moeda brasileira, removendo separadores de milhar.
            """
            valor_formatado = f"{valor:.2f}".replace(".", ",")
            return valor_formatado
        
         # Chamar fatura passando todos os parâmetros necessários
        if fatura(navegador, 'faturado.png'):
            print(f"Pedido R$ {Pedido} do valor {Value_Titulo} não foi faturado")
            tabela_produtos.at[linha, "statuns"] = "não faturado"
            tabela_produtos.to_excel(caminho_arquivo, sheet_name="Cascavel", index=False)
            time.sleep(3)
            return
        else:
            print("Tudo certo, seguindo para o fluxo")


        #Clicar em Baixas
        esperar_e_clicar(navegador, 'COMP4598')
        time.sleep(5)

         #Aqui vai Esperar o campo de baixas aparecer, se der errado, ele vai clicar em baixar e esperar
        try:
            ##Esperara Baixass
            imagem_alvo = 'espearar_aparecer.png'
            esperar_imagem_aparecer(navegador, imagem_alvo)
            time.sleep(2)

        except Exception as e:
            print(f"Erro ao clicar em 'não': {e}")
            
            try:
                #Clicar em Baixas
                esperar_e_clicar(navegador, 'COMP4598')
                time.sleep(5)
                
                ##Esperara Baixass
                imagem_alvo = 'espearar_aparecer.png'
                esperar_imagem_aparecer(navegador, imagem_alvo)
                time.sleep(2)
            except Exception as e:
                print(f"Erro ao Esperar a tela de baixas: {e}")

        #Colocar o banco
        inserir_Sem_Espaço(navegador,'COMP6031',Bank)
        time.sleep(1)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(1)

        #Colocar Conta
        inserir_Sem_Espaço(navegador,'COMP6035',Cont)
        time.sleep(3)

        inserir_Sem_Espaço(navegador,'COMP6041', Hist)
        time.sleep(2)

        desc ="0,00"
        # Apagar descontos
        inserir_Com_Python(navegador, 'COMP6059', desc)
        time.sleep(2)

        # Apagar Multa
        inserir_Com_Python(navegador, 'COMP6061', desc)
        time.sleep(2)

        
        # Apagar TX Perman
        inserir_Com_Python(navegador, 'COMP6063', Juros)
        time.sleep(3)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        
        #Clicar em Salvar
        esperar_e_clicar(navegador,'COMP6076')
        time.sleep(1)

         #Aqui vai clica em não, se der erro vai clicar em salvar e depois em não
        try:
            ##Esperara Baixass
            imagem_alvo = 'nao.png'
            esperar_imagem_aparecer(navegador, imagem_alvo)
            time.sleep(1)

            #Clicar em não
            esperar_e_clicar(navegador,'COMP6013')
            time.sleep(1)

            tabela_produtos.at[linha, "statuns"] = "OK"
            tabela_produtos.to_excel(caminho_arquivo, sheet_name="Cascavel", index=False)
            time.sleep(5)

        except Exception as e:
            print(f"Erro ao clicar em 'não': {e}")
            
            try:
                #Clicar em Salvar
                esperar_e_clicar(navegador,'COMP6076')
                time.sleep(1)
                
                #Clicar em não
                esperar_e_clicar(navegador,'COMP6013')
                time.sleep(5)

                tabela_produtos.at[linha, "statuns"] = "OK"
                tabela_produtos.to_excel(caminho_arquivo, sheet_name="Cascavel", index=False)
                time.sleep(5)

            except Exception as e:
                print(f"Erro ao tentar clicar não e depois em salvar: {e}")

    except Exception as e:
        print(f"Erro na linha {linha}: {e}") 

for linha in tabela_produtos.index:
    processar_linha(linha)

print('Processo concluído!')




