from selenium import webdriver
import cv2
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import shutil
from datetime import datetime, timedelta
import re
import subprocess
import zipfile


# Obter datas necessárias
hoje = datetime.now()
hoje_formatado = f"{hoje.year}{hoje.month:02d}{hoje.day:02d}"
print(hoje_formatado)
cnpj =  '10.319.780/0018-3'
valor = "2700,00"
valor_formatado = valor
print(valor_formatado)

cliente = "METAL CENTER"

# Caminho para a extensão .crx
EXTENSAO = r"C:\Users\Adryan.Cordeiro\OneDrive - Gimave\Área de Trabalho\Gestão_Ctt\captcha\captcha.crx"

# Caminho para salvar downloads
download_path = r"C:\Users\Adryan.Cordeiro\OneDrive - Gimave\Área de Trabalho\Gestão_Ctt"

def extrair_e_renomear(arquivo_zip, diretorio_destino, nome_base):
    """
    Extrai arquivos de um arquivo ZIP e os renomeia de acordo com o nome base fornecido.

    :param arquivo_zip: Caminho do arquivo ZIP a ser extraído.
    :param diretorio_destino: Diretório onde os arquivos extraídos serão armazenados.
    :param nome_base: Nome base para os arquivos extraídos, que será usado para renomeá-los.
    :return: Lista com os caminhos dos arquivos extraídos e renomeados.
    """
    arquivos_extraidos = []
    
    # Criar o diretório de destino, caso não exista
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)
    
    try:
        # Abrir o arquivo ZIP
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            # Extrair todos os arquivos para o diretório de destino
            zip_ref.extractall(diretorio_destino)
            print(f"Arquivos extraídos para: {diretorio_destino}")
            
            # Renomear os arquivos extraídos
            for nome_arquivo in zip_ref.namelist():
                caminho_arquivo_antigo = os.path.join(diretorio_destino, nome_arquivo)
                
                # Criar o novo nome para o arquivo
                nome_novo = f"{nome_base}_{nome_arquivo}"
                nome_novo = re.sub(r'[^\w\s.-]', '_', nome_novo)  # Substitui caracteres especiais por _
                
                caminho_arquivo_novo = os.path.join(diretorio_destino, nome_novo)
                
                # Renomear o arquivo
                os.rename(caminho_arquivo_antigo, caminho_arquivo_novo)
                arquivos_extraidos.append(caminho_arquivo_novo)
                print(f"Arquivo renomeado para: {caminho_arquivo_novo}")
    
    except Exception as e:
        print(f"Erro ao extrair ou renomear arquivos: {e}")
        raise
    
    return arquivos_extraidos

def configurar_navegador(download_path, extensao):
    """
    Configura e retorna uma instância do navegador Chrome com extensões e preferências de download.
    """
    options = Options()

     # Adicionar o modo headless para não abrir a janela
     #options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Desabilita aceleração de GPU (necessário em alguns casos)

    # Configurar as preferências de download
    prefs = {
        "download.default_directory": download_path,  # Diretório de download
        "download.prompt_for_download": False,         # Impede o prompt de download
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,                   # Habilita navegação segura
        "plugins.always_open_pdf_externally": True     # Abrir PDF externamente sem prompt
    }
    options.add_experimental_option("prefs", prefs)
    
    # Adicionar a extensão
    options.add_extension(extensao)
    
    # Inicializar o serviço e o driver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def esperar_clicar_limpar(driver, xpath, tempo_espera=30):
    """
    Espera até que o elemento identificado pelo XPath seja clicável, clica e limpa o campo.

    :param driver: Instância do WebDriver.
    :param xpath: XPath do elemento a ser manipulado.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    """
    try:
        # Aguarda até que o elemento seja clicável
        elemento = WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        # Clica no elemento
        elemento.click()
        print("Elemento clicado com sucesso.")

        # Verifica se o elemento é do tipo que pode ser limpo
        if elemento.tag_name in ['input', 'textarea']:
            elemento.clear()
            print("Campo limpo com sucesso.")
        else:
            print("O elemento não suporta a operação de limpeza.")
    except Exception as e:
        print(f"Erro ao clicar ou limpar o elemento: {e}")


def esperar_e_clicar(driver, by, value, timeout=30):
    """
    Aguarda até que o elemento esteja clicável e realiza o clique.
    """
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        elemento.click()
        print(f"Elemento clicado: {value}")
    except Exception as e:
        print(f"Erro ao clicar no elemento {value}: {e}")
        raise

def esperar_e_inserir_texto(driver, by, value, texto, timeout=30):
    """
    Aguarda até que o elemento esteja visível, limpa o campo e insere o texto especificado.
    """
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))
        elemento.clear()
        elemento.send_keys(texto)
        print(f"Texto inserido no elemento {value}: {texto}")
    except Exception as e:
        print(f"Erro ao inserir texto no elemento {value}: {e}")
        raise

def esperar_download_arquivo(download_path, nome_arquivo, timeout=60):
    """
    Espera até que o arquivo seja baixado no diretório de download.

    :param download_path: Caminho do diretório de download.
    :param nome_arquivo: Nome do arquivo a ser baixado.
    :param timeout: Tempo máximo de espera em segundos (padrão: 60 segundos).
    :return: Caminho completo do arquivo baixado ou None se o download falhar.
    """
    caminho_arquivo = os.path.join(download_path, nome_arquivo)
    tempo_espera = 0
    while tempo_espera < timeout:
        if os.path.exists(caminho_arquivo):
            print(f"Arquivo {nome_arquivo} baixado com sucesso!")
            return caminho_arquivo
        time.sleep(1)  # Espera 1 segundo antes de verificar novamente
        tempo_espera += 1
    print(f"Erro: O arquivo {nome_arquivo} não foi baixado dentro do tempo limite.")
    return None

def fechar_abas_exceto_a_principal(driver, url_principal):
    """
    Fecha todas as abas abertas, exceto a aba principal que contém a URL especificada.
    """
    # Obter todas as janelas/abas abertas
    todas_abas = driver.window_handles
    
    for aba in todas_abas:
        driver.switch_to.window(aba)  # Mudar para a aba atual
        if driver.current_url != url_principal:
            driver.close()  # Fechar a aba se não for a principal

IMAGEM_ALVO = "bot.png"
def detectar_e_clicar_imagem(driver, imagem_alvo, timeout=30):
    """
    Detecta uma imagem no navegador e clica no local correspondente.
    """
    try:
        import os
        
        # Verificar se a imagem alvo existe
        if not os.path.exists(imagem_alvo):
            raise FileNotFoundError(f"Imagem alvo não encontrada: {imagem_alvo}")
        
        # Esperar pelo carregamento da página
        WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))

        # Captura de tela do navegador
        screenshot = driver.get_screenshot_as_png()
        screen_array = np.frombuffer(screenshot, dtype=np.uint8)
        screen_image = cv2.imdecode(screen_array, cv2.IMREAD_COLOR)  # Garantir leitura em cores
        
        # Converter a captura de tela para escala de cinza
        screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
        
        # Carregar a imagem do template e converter para escala de cinza
        template = cv2.imread(imagem_alvo, cv2.IMREAD_COLOR)
        if template is None:
            raise ValueError(f"Erro ao carregar a imagem do template: {imagem_alvo}")
        
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        # Realizar a correspondência de template
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        
        # Configuração do limite para correspondência
        threshold = 0.8  # 80% de correspondência
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            print(f"Imagem encontrada com {max_val*100:.2f}% de correspondência!")
            
            # Calcular as coordenadas do clique
            template_h, template_w = template_gray.shape[:2]
            click_x = max_loc[0] + template_w // 2
            click_y = max_loc[1] + template_h // 2
            
            # Aguardar um pouco antes de clicar
            time.sleep(1)  # Ajuste o tempo se necessário
            
            # Simular o clique no navegador diretamente
            driver.execute_script(f"window.scrollTo({click_x}, {click_y});")
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_by_offset(click_x, click_y).click().perform()
            
        else:
            print("Imagem não encontrada na tela.")
    
    except Exception as e:
        print(f"Erro ao detectar ou clicar na imagem: {e}")
        raise


def main():
    try:
        navegador = configurar_navegador(download_path, EXTENSAO)
        navegador.get("https://nfse-cascavel.atende.net/autoatendimento/servicos/nfse")
        
        # Login
        esperar_e_inserir_texto(navegador, By.XPATH, '/html/body/div[1]/div[2]/span[3]/input', "05.989.476/0001-10")

        #Senha
        esperar_e_inserir_texto(navegador, By.XPATH, '/html/body/div[1]/div[2]/span[5]/div/input', "Gim@ve2025")

        #Clicar para Entrar
        esperar_e_clicar(navegador, By.XPATH, '/html/body/div[1]/div[2]/span[7]/button')
        time.sleep(3)
        
        # Clicar em "Acessar"
        esperar_e_clicar(navegador, By.XPATH, '//a[@title="Atende.net"]')
        time.sleep(5)
        
        # Clicar na caixa do reCAPTCHA
        detectar_e_clicar_imagem(navegador, IMAGEM_ALVO)
        time.sleep(5)

        # Clicar em um botão dentro da interface da extensão
        actions = ActionChains(navegador)
        # Pressionar Shift duas vezes
        actions.key_down(Keys.TAB).perform()  # Pressionar TAB
        time.sleep(1)
        actions.key_down(Keys.TAB).perform()  # Pressionar TAB
        time.sleep(1)

        #Clicar na Extensão
        actions.send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(15)

        # No seu fluxo, logo antes de acessar a página de gerenciamento de notas, use a função:
        fechar_abas_exceto_a_principal(navegador, "https://nfse-cascavel.atende.net/?rot=1&aca=1#!/sistema/66")
        time.sleep(5)

        #Clicar em Gerenciamento 
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="conteudo_66079_1063_1"]/div/span[1]/fieldset/div/div/span[2]/article/div[2]')
        time.sleep(5)

       # Limpar Data
        esperar_clicar_limpar(navegador, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input')
        time.sleep(3)

        # Colocar Data Mês 06
        elemento = WebDriverWait(navegador, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input')))
        # Caso o campo seja do tipo 'date', use JavaScript para preencher
        navegador.execute_script("arguments[0].value = '01/06/2024';", elemento)
        time.sleep(1)


        #Colocar Cnpj:
        esperar_e_inserir_texto(navegador, By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[3]/tbody/tr/td[2]/span/input[2]', cnpj)
        time.sleep(7)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(1)

        #Clicar em Filtro:
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[2]/span/div/div/table/tbody/tr[2]/td[1]/select')
        time.sleep(1)

        #Clicar em Valor:
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[2]/span/div/div/table/tbody/tr[2]/td[1]/select/option[13]')
        time.sleep(1)

        #Inserir Valor
        esperar_e_inserir_texto(navegador, By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[2]/span/div/div/table/tbody/tr[2]/td[3]/input', valor)
        time.sleep(1)

        #Clicar em Consulta:
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[3]/table/tbody/tr/td[3]/div/span/span[2]')
        time.sleep(10)

        #Selecionar Ferramentas
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/header/div[2]/table/tbody/tr[1]/td[1]/button')
        time.sleep(2)

        #Clicar em Dowlond
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[2]/div[1]/span[2]/span[1]')
        time.sleep(2)

        #Clicar em PDF
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="context_menu"]/table/tbody/tr[1]/td/span')
        time.sleep(2)

        #Clicar em PDF
        esperar_e_clicar(navegador, By.XPATH, '//*[@id="estrutura_container_sistema"]/div[4]/section/footer/button[1]')
        time.sleep(5)

       # Nome do arquivo que será baixado
        nf_baixada = f"EXPORTACAO_NFSE_{hoje_formatado}_PDF.zip"

        # Esperar até que o arquivo seja baixado
        caminho_arquivo = esperar_download_arquivo(download_path, nf_baixada)

        if caminho_arquivo:
            # Renomear o arquivo baixado
            diretorio_extraidos = r"C:\Users\Adryan.Cordeiro\OneDrive - Gimave\Área de Trabalho\Gestão_Ctt\Extraidos"
            nome_base = f"Cliente {cliente} - CNPJ {cnpj} - VALOR {valor_formatado}.zip"
            nome_base = re.sub(r'[^\w\s.-]', '_', nome_base)
            caminho_destino = os.path.join(download_path, nome_base + ".zip")

            contador = 1
            arquivo_destino_temp = caminho_destino

            while os.path.exists(arquivo_destino_temp):
                arquivo_destino_temp = caminho_destino.replace(".zip", f"_{contador}.zip")
                contador += 1

            os.rename(caminho_arquivo, arquivo_destino_temp)
            print(f"O arquivo foi renomeado para: {arquivo_destino_temp}")

            # Restante do código para extração e renomeio dos arquivos PDF
            arquivos_extraidos = extrair_e_renomear(arquivo_destino_temp, diretorio_extraidos, nome_base)

            # Remover o arquivo ZIP após extração
            os.remove(arquivo_destino_temp)
            print(f"O arquivo ZIP foi apagado: {arquivo_destino_temp}")

            # Abrir todos os arquivos extraídos
            for arquivo in arquivos_extraidos:
                os.startfile(arquivo)
    finally:
        if 'navegador' in locals() and navegador:
            navegador.quit()


if __name__ == "__main__":
    main()
