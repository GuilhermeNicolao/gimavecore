from csv import writer
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import shutil
from datetime import datetime
from selenium.webdriver.common.keys import Keys


# Caminho para a pasta de Downloads e para a pasta de destino
pasta_downloads = r"C:\Users\Natanael.Alencar\Downloads"
pasta_destino = r"C:\Users\Natanael.Alencar\Desktop\Extratos_CIELO"

# Definir os dias da semana
dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

# Datas relevantes
hoje = datetime.now()
ontem = hoje - timedelta(days=1)
anteontem = hoje - timedelta(days=2)
antes_anteontem = hoje - timedelta(days=3)


# Formatação Dia, Mês, Ano (com ano completo) e Dia da Semana
dia_da_semana_atual = dias_da_semana[hoje.weekday()]
hoje_formatado = f"{hoje.day:02d}-{hoje.month:02d}-{hoje.year}"  # Ano completo
ontem_formatado = f"{ontem.day:02d}-{ontem.month:02d}-{ontem.year}"  # Ano completo
anteontem_formatado = f"{anteontem.day:02d}-{anteontem.month:02d}-{anteontem.year}"  # Ano completo
antes_anteontem_formatado = f"{antes_anteontem.day:02d}-{antes_anteontem.month:02d}-{antes_anteontem.year}"  # Ano completo

# Exibe os resultados no formato DD/MM/AAAA
print(f"Ontem foi {ontem_formatado}")
print(f"Antes de ontem foi {anteontem_formatado}")
print(f"Hoje é {hoje_formatado}")
print(f"O dia da semana hoje é {dia_da_semana_atual}")


def renomear_e_mover_ultimo_arquivo_0533():
    # Verifica todos os arquivos na pasta de Downloads
    arquivos = [os.path.join(pasta_downloads, f) for f in os.listdir(pasta_downloads) if os.path.isfile(os.path.join(pasta_downloads, f))]
    
    # Se houver arquivos na pasta
    if arquivos:
        # Encontra o arquivo mais recente com base na data de modificação
        ultimo_arquivo = max(arquivos, key=os.path.getmtime)

        # Obter a data atual para gerar o novo nome
        data_atual = hoje_formatado
        
        # Cria o novo nome do arquivo com base na data
        novo_nome = f"Vendas EC 0533 -{ontem_formatado}.xlsx"
        
        # Caminho completo do novo arquivo
        novo_caminho = os.path.join(pasta_destino, novo_nome)
        
        try:
            # Mover e renomear o arquivo
            shutil.move(ultimo_arquivo, novo_caminho)
            print(f"Arquivo '{ultimo_arquivo}' renomeado para '{novo_caminho}' e movido com sucesso.")
        except Exception as e:
            print(f"Erro ao mover o arquivo: {e}")
    else:
        print("Nenhum arquivo encontrado na pasta de Downloads.")

def renomear_e_mover_ultimo_arquivo_0533_anteontem():
    # Verifica todos os arquivos na pasta de Downloads
    arquivos = [os.path.join(pasta_downloads, f) for f in os.listdir(pasta_downloads) if os.path.isfile(os.path.join(pasta_downloads, f))]
    
    # Se houver arquivos na pasta
    if arquivos:
        # Encontra o arquivo mais recente com base na data de modificação
        ultimo_arquivo = max(arquivos, key=os.path.getmtime)

        # Obter a data atual para gerar o novo nome
        data_atual = hoje_formatado
        
        # Cria o novo nome do arquivo com base na data
        novo_nome = f"Vendas EC 0533 -{anteontem_formatado}.xlsx"
        
        # Caminho completo do novo arquivo
        novo_caminho = os.path.join(pasta_destino, novo_nome)
        
        try:
            # Mover e renomear o arquivo
            shutil.move(ultimo_arquivo, novo_caminho)
            print(f"Arquivo '{ultimo_arquivo}' renomeado para '{novo_caminho}' e movido com sucesso.")
        except Exception as e:
            print(f"Erro ao mover o arquivo: {e}")
    else:
        print("Nenhum arquivo encontrado na pasta de Downloads.")

def renomear_e_mover_ultimo_arquivo_0533_antes_anteontem():
    # Verifica todos os arquivos na pasta de Downloads
    arquivos = [os.path.join(pasta_downloads, f) for f in os.listdir(pasta_downloads) if os.path.isfile(os.path.join(pasta_downloads, f))]
    
    # Se houver arquivos na pasta
    if arquivos:
        # Encontra o arquivo mais recente com base na data de modificação
        ultimo_arquivo = max(arquivos, key=os.path.getmtime)

        # Obter a data atual para gerar o novo nome
        data_atual = hoje_formatado
        
        # Cria o novo nome do arquivo com base na data
        novo_nome = f"Vendas EC 0533 -{antes_anteontem_formatado}.xlsx"
        
        # Caminho completo do novo arquivo
        novo_caminho = os.path.join(pasta_destino, novo_nome)
        
        try:
            # Mover e renomear o arquivo
            shutil.move(ultimo_arquivo, novo_caminho)
            print(f"Arquivo '{ultimo_arquivo}' renomeado para '{novo_caminho}' e movido com sucesso.")
        except Exception as e:
            print(f"Erro ao mover o arquivo: {e}")
    else:
        print("Nenhum arquivo encontrado na pasta de Downloads.")

def renomear_e_mover_ultimo_arquivo_rec_0533():
    # Verifica todos os arquivos na pasta de Downloads
    arquivos = [os.path.join(pasta_downloads, f) for f in os.listdir(pasta_downloads) if os.path.isfile(os.path.join(pasta_downloads, f))]
    
    # Se houver arquivos na pasta
    if arquivos:
        # Encontra o arquivo mais recente com base na data de modificação
        ultimo_arquivo = max(arquivos, key=os.path.getmtime)

        # Obter a data atual para gerar o novo nome
        data_atual = hoje_formatado
        
        # Cria o novo nome do arquivo com base na data
        novo_nome = f"Recebiveis EC 0533 -{hoje_formatado}.xlsx"
        
        # Caminho completo do novo arquivo
        novo_caminho = os.path.join(pasta_destino, novo_nome)
        
        try:
            # Mover e renomear o arquivo
            shutil.move(ultimo_arquivo, novo_caminho)
            print(f"Arquivo '{ultimo_arquivo}' renomeado para '{novo_caminho}' e movido com sucesso.")
        except Exception as e:
            print(f"Erro ao mover o arquivo: {e}")
    else:
        print("Nenhum arquivo encontrado na pasta de Downloads.")


# Configuração para o diretório de download
download_diretorio = r"C:\Users\Natanael.Alencar\Desktop\Extratos_CIELO"

# Configurar opções do Chrome para o diretório de download
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_diretorio,  # Define o diretório padrão
    "download.prompt_for_download": False,            # Não perguntar pelo local do download
    "download.directory_upgrade": True,               # Atualizar o diretório padrão
    "safebrowsing.enabled": True                      # Habilitar proteção contra downloads inseguros
})

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

def esperar_e_clicar(driver, xpath, tempo_espera=30):
    """
    Espera até que o elemento identificado pelo XPath seja clicável e, então, clica.
    
    :param driver: Instância do WebDriver.
    :param xpath: XPath do elemento a ser clicado.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    """
    try:
        elemento = WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elemento.click()
        print('Elemento Clicado Com sucesso')
    except Exception as e:
        print(f"Erro ao clicar no elemento: {e}")

def esperar_e_inserir_texto(driver, xpath, texto, tempo_espera=30):
    """
    Espera até que o elemento identificado pelo XPath seja visível e, então, insere o texto.
    
    :param driver: Instância do WebDriver.
    :param xpath: XPath do elemento onde o texto será inserido.
    :param texto: Texto a ser inserido no elemento.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    """
    try:
        elemento = WebDriverWait(driver, tempo_espera).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        elemento.clear()  # Limpa o campo de texto antes de inserir os dados
        elemento.send_keys(texto)
    except Exception as e:
        print(f"Erro ao inserir texto no elemento: {e}")
        
# Instalar e configurar o WebDriver
servico = Service(ChromeDriverManager().install())

# Iniciar o navegador Chrome com o serviço
navegador = webdriver.Chrome(service=servico)
# Abrir Link
navegador.get("https://minhaconta2.cielo.com.br/site/acessos/login")
acoes = ActionChains(navegador)

print("Configurações do Chrome:")
print(navegador.capabilities.get('goog:chromeOptions'))

def fechar_popup_anuncio(driver, xpath, tempo_espera=30):
    """
    Espera até que o botão de fechar do pop-up ou anúncio esteja visível e clica para fechar.

    :param driver: Instância do WebDriver.
    :param xpath: XPath do botão de fechar do pop-up ou anúncio.
    :param tempo_espera: Tempo máximo de espera em segundos (padrão: 30 segundos).
    """
    try:
        # Espera até que o botão de fechar esteja visível
        botao_fechar = WebDriverWait(driver, tempo_espera).until(
            EC.visibility_of_element_located((By.XPATH, xpath))  # Verifique visibilidade
        )
        # Verifica se o botão de fechar está clicável
        WebDriverWait(driver, tempo_espera).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        botao_fechar.click()
        print("Pop-up ou anúncio fechado com sucesso.")
    except Exception as e:
        print(f"Erro ao tentar fechar o pop-up ou anúncio: {e}")


# Preencher Usuário e Senha
esperar_e_inserir_texto (navegador , '//*[@id="loginMainField"]/div/input' , "032.961.829-69")
esperar_e_clicar(navegador,'//*[@id="bt-submit"]')
esperar_e_inserir_texto(navegador,'//*[@id="flui-input-v2-1"]/div/input',"789070")
esperar_e_clicar(navegador, '//*[@id="bt-submit"]')
time.sleep(10)

# Fechar pop-up de anúncios, se aparecer
fechar_popup_anuncio(navegador, '//*[@id="0"]/div/ng-transclude/div/div/a')

# Clicar em Meus Estabelecimentos
esperar_e_clicar(navegador, '//*[@id="menu-change-ec"]/ng-include[1]/div/div[2]/div[2]/div/div/div/span')
time.sleep(1)

# Clicar em Ver Mais
esperar_e_clicar(navegador, '//*[@id="list-tree-content"]/merchant-item[1]/div/div/div[5]/div')
time.sleep(2)

# Fechar pop-up de anúncios, se aparecer
fechar_popup_anuncio(navegador, '/html/body/div[7]/div/footer-site/cookies-alert/div/div/flui-button/div')

# Mais Estabelecimentos
esperar_e_clicar(navegador, '/html/body/div[1]/div/div/div/div/div/merchant-view-mode/div/div[4]/view-list[1]/div/div[2]/flui-button/div/ng-transclude/span')

# Função para rolar até o elemento
def rolar_para_elemento(navegador, xpath):
    try:
        # Espera até o elemento estar presente na página
        elemento = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # Rola até o elemento utilizando JavaScript
        navegador.execute_script("arguments[0].scrollIntoView();", elemento)
    except Exception as e:
        print("Erro ao rolar até o elemento:", e)

# Exemplo de uso da função
rolar_para_elemento(navegador, '//*[@id="0"]/div/ng-transclude/div/div/a')

#Clicar no EC 0533
esperar_e_clicar(navegador, '//*[@id="list-tree-content"]/div[26]/div[1]')

#Clicar em acessar
esperar_e_clicar(navegador, '/html/body/div[1]/div/div/div/div/div/merchant-view-mode/div/div[5]/flui-button[2]/div/ng-transclude/span')
time.sleep(3)

# Fechar pop-up de anúncios, se aparecer
fechar_popup_anuncio(navegador, '//*[@id="0"]/div/ng-transclude/div/div/a')

#Clicar em Vendas 
esperar_e_clicar(navegador, '//*[@id="navbar"]/ul/li[2]/a/div')
time.sleep(2)

#Clicar em minhas vendas
esperar_e_clicar(navegador, '//*[@id="navbar"]/ul/li[2]/ul/div[2]/div/ul/li[1]')
time.sleep(5)

#Clicar em Detalhado
esperar_e_clicar(navegador, '//*[@id="btn-detalhado"]/label')
time.sleep(2)

#Verificar se data for Segunda

if dia_da_semana_atual == 'Segunda':
    print('Hoje é segunda, executando as 3 datas')

    #Clicar em Data da Venda
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')

    #Processo de Verificação de data (ontem)

    #Escolher Histórico de Vendas 
    esperar_e_clicar(navegador, '//*[@id="toggle-histórico"]')
    time.sleep(5)

    # Localizar o elemento de data pelo XPath
    elemento_data = navegador.find_element(By.XPATH, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')

    # Cria a ação de clicar 3 vezes no campo de data (para selecionar o texto)
    acoes = ActionChains(navegador)
    acoes.click(elemento_data).click(elemento_data).click(elemento_data).perform()
    acoes.send_keys(Keys.BACKSPACE).perform()
    time.sleep(2)


    # Escrever a nova data no campo
    # Se o campo precisa da data no formato YYYY-MM-DD
    print(f"Data a ser inserida: {ontem_formatado}")  # Verifique o formato da data
    time.sleep(5)

    # Inserir a data corretamente no campo
    elemento_data.send_keys(ontem_formatado, ontem_formatado)

    # Clicar no botão confirmar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div/div/div[2]/div[5]/div[2]/div[2]/label/button')
    time.sleep(1)

    # Clicar no botão Exportar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/label/button')
    time.sleep(1)

    # Clicar e escolher Excel
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]')
    time.sleep(1)

    # Clicar em Avançar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
    time.sleep(1)

    #Clicar em Avançar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
    time.sleep(2)

    #Clicar Acessar relatórios
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/button')
    time.sleep(5)

    #Clicar Baixar Relatórios 
    esperar_e_clicar(navegador, '//*[@id="scroll-container"]/div/div/div/tr[1]/td[5]/div/i')
    time.sleep(5)

    # Aguardar um tempo para garantir que o arquivo tenha sido baixado (se necessário)

    # Chamar a função para mover e renomear o último arquivo
    renomear_e_mover_ultimo_arquivo_0533()
    time.sleep(5)

    # Fechar Relatorios 
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[4]/div/div[3]/div/div[2]/div/button')
    time.sleep(5)

    #Processo de Verificação de data (Antes de ontem)

    #Clicar em Data da Venda
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')
    time.sleep(5)

    # Localizar o elemento de data pelo XPath
    elemento_data = navegador.find_element(By.XPATH, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')

    # Cria a ação de clicar 3 vezes no campo de data (para selecionar o texto)
    acoes = ActionChains(navegador)
    acoes.click(elemento_data).click(elemento_data).click(elemento_data).perform()
    acoes.send_keys(Keys.BACKSPACE).perform()
    time.sleep(2)


    # Escrever a nova data no campo
    # Se o campo precisa da data no formato YYYY-MM-DD
    print(f"Data a ser inserida: {anteontem_formatado}")  # Verifique o formato da data
    time.sleep(5)

    # Inserir a data corretamente no campo
    elemento_data.send_keys(anteontem_formatado, anteontem_formatado)

    # Clicar no botão confirmar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div/div/div[2]/div[5]/div[2]/div[2]/label/button')
    time.sleep(1)

    # Clicar no botão Exportar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/label/button')
    time.sleep(1)

    # Clicar e escolher Excel
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]')
    time.sleep(1)

    # Clicar em Avançar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
    time.sleep(1)

    #Clicar em Avançar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
    time.sleep(2)

    #Clicar Acessar relatórios
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/button')
    time.sleep(5)

    #Clicar Baixar Relatórios 
    esperar_e_clicar(navegador, '//*[@id="scroll-container"]/div/div/div/tr[1]/td[5]/div/i')
    time.sleep(5)

    # Aguardar um tempo para garantir que o arquivo tenha sido baixado (se necessário)

    # Chamar a função para mover e renomear o último arquivo
    renomear_e_mover_ultimo_arquivo_0533_anteontem()
    time.sleep(5)

    # Fechar Relatorios 
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[4]/div/div[3]/div/div[2]/div/button')
    time.sleep(5)

    #processo verificação de Data (Antes de Anteontem)

    #Processo de Verificação de data (Antes de ontem)

    #Clicar em Data da Venda
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')
    time.sleep(5)

    # Localizar o elemento de data pelo XPath
    elemento_data = navegador.find_element(By.XPATH, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')

    # Cria a ação de clicar 3 vezes no campo de data (para selecionar o texto)
    acoes = ActionChains(navegador)
    acoes.click(elemento_data).click(elemento_data).click(elemento_data).perform()
    acoes.send_keys(Keys.BACKSPACE).perform()
    time.sleep(2)


    # Escrever a nova data no campo
    # Se o campo precisa da data no formato YYYY-MM-DD
    print(f"Data a ser inserida: {antes_anteontem_formatado}")  # Verifique o formato da data
    time.sleep(5)

    # Inserir a data corretamente no campo
    elemento_data.send_keys(antes_anteontem_formatado, antes_anteontem_formatado)

    # Clicar no botão confirmar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div/div/div[2]/div[5]/div[2]/div[2]/label/button')
    time.sleep(1)

    # Clicar no botão Exportar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/label/button')
    time.sleep(1)

    # Clicar e escolher Excel
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]')
    time.sleep(1)

    # Clicar em Avançar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
    time.sleep(1)

    #Clicar em Avançar
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
    time.sleep(2)

    #Clicar Acessar relatórios
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/button')
    time.sleep(5)

    #Clicar Baixar Relatórios 
    esperar_e_clicar(navegador, '//*[@id="scroll-container"]/div/div/div/tr[1]/td[5]/div/i')
    time.sleep(5)

    # Aguardar um tempo para garantir que o arquivo tenha sido baixado (se necessário)

    # Chamar a função para mover e renomear o último arquivo
    renomear_e_mover_ultimo_arquivo_0533_antes_anteontem()
    time.sleep(5)

    # Fechar Relatorios 
    esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[4]/div/div[3]/div/div[2]/div/button')
    time.sleep(5)

else : 

        #Clicar em Data da Venda
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')


        #Escolher Histórico de Vendas 
        esperar_e_clicar(navegador, '//*[@id="toggle-histórico"]')
        time.sleep(5)

        # Localizar o elemento de data pelo XPath
        elemento_data = navegador.find_element(By.XPATH, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div/div/span[1]/input')

        # Cria a ação de clicar 3 vezes no campo de data (para selecionar o texto)
        acoes = ActionChains(navegador)
        acoes.click(elemento_data).click(elemento_data).click(elemento_data).perform()
        acoes.send_keys(Keys.BACKSPACE).perform()
        time.sleep(2)


        # Escrever a nova data no campo
        # Se o campo precisa da data no formato YYYY-MM-DD
        print(f"Data a ser inserida: {ontem_formatado}")  # Verifique o formato da data
        time.sleep(5)

        #Inserir a data corretamente no campo
        elemento_data.send_keys(ontem_formatado, ontem_formatado)

        #Clicar no botão confirmar
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[3]/div/div/div/div[2]/div[5]/div[2]/div[2]/label/button')
        time.sleep(1)

        #Clicar no botão Exportar
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/label/button')
        time.sleep(1)

        #Clicar e escolher Excel
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]')
        time.sleep(1)

        #Clicar em Avançar
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
        time.sleep(1)

        #Clicar em Avançar
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[3]/div[2]/button')
        time.sleep(2)

        #Clicar Acessar relatórios
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/button')
        time.sleep(5)

        #Clicar Baixar Relatórios 
        esperar_e_clicar(navegador, '//*[@id="scroll-container"]/div/div/div/tr[1]/td[5]/div/i')
        time.sleep(5)

        # Aguardar um tempo para garantir que o arquivo tenha sido baixado (se necessário)

        # Chamar a função para mover e renomear o último arquivo
        renomear_e_mover_ultimo_arquivo_0533()
        time.sleep(5)

        # Fechar Relatorios 
        esperar_e_clicar(navegador, '/html/body/app-root/app-layout/mft-wc-wrapper/div/vendas-element/div[2]/div[2]/div/div[4]/div/div[3]/div/div[2]/div/button')
        time.sleep(5)

# Clicar em Recebiveis
esperar_e_clicar (navegador,'/html/body/app-root/app-layout/app-header/div/div/app-header-menu/ul/li[3]/div')
time.sleep(5)

# Clicar em Detalhado
esperar_e_clicar (navegador,'//*[@id="btn-detalhado"]/label')
time.sleep(5)

# Clicar em Exportar 
esperar_e_clicar(navegador,'/html/body/app-root/app-layout/mft-wc-wrapper/div/recebiveis-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/label/button')
time.sleep(2)

# Escolher formato de arquivo 
esperar_e_clicar(navegador,'/html/body/app-root/app-layout/mft-wc-wrapper/div/recebiveis-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]')
time.sleep(2)

# clicar em avançar 
esperar_e_clicar(navegador,'/html/body/app-root/app-layout/mft-wc-wrapper/div/recebiveis-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/button')
time.sleep(2)

# Acessar Relatorios
esperar_e_clicar(navegador,'/html/body/app-root/app-layout/mft-wc-wrapper/div/recebiveis-element/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/button')
time.sleep(2)

# Baixar arquivo
esperar_e_clicar(navegador,'//*[@id="scroll-container"]/div/div/div/tr[1]/td[5]')
time.sleep(2)

#Clicar em fechar 
esperar_e_clicar(navegador,'/html/body/app-root/app-layout/mft-wc-wrapper/div/recebiveis-element/div[2]/div[2]/div/div[4]/div/div[3]/div/div[2]/div/button')
time.sleep(5)

#Exportar arquivo da Pasta downloads para pasta Extrato
renomear_e_mover_ultimo_arquivo_rec_0533()
time.sleep(5)

# Fechar o navegador após concluir todas as operações
navegador.quit()


