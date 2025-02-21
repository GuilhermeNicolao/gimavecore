import time
import os
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Configurações do Chrome para download
options = webdriver.ChromeOptions()
download_path = r"C:\Users\Guilherme.Silva\Desktop"
options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Instala e configura o WebDriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)

# Obter datas necessárias
hoje = datetime.now()
ontem = hoje - timedelta(days=1)
amanha = hoje + timedelta(days=1)
Sete = hoje - timedelta(days=7)
hoje_formatado = f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year}"
ontem_formatado = f"{ontem.day:02d}/{ontem.month:02d}/{ontem.year}"
amanha_formatado = f"{amanha.day:02d}/{amanha.month:02d}/{amanha.year}"
Sete_Dias = f"{Sete.day:02d}/{Sete.month:02d}/{Sete.year}"

load_dotenv()

# Acessar a página de relatórios

navegador.get("https://portaleucard.virtusinfo.com.br:8443/SGC/relatorios/contas_receber/relatorio.xhtml")

# Preencher Usuário e Senha
navegador.find_element(By.XPATH, '//*[@id="formLogin:Usuario"]').send_keys(os.getenv("LOGIN"))
navegador.find_element(By.XPATH, '//*[@id="formLogin:senha"]').send_keys(os.getenv("PW2"))
navegador.find_element(By.XPATH, '//*[@id="formLogin:j_idt24"]/span').click()

time.sleep(2)

navegador.get("https://portaleucard.virtusinfo.com.br:8443/SGC/relatorios/pedido_diario/relatorio.xhtml")

# Espera explícita para garantir que o elemento esteja presente
wait = WebDriverWait(navegador, 10)

# Preencher datas no formulário
data_inicio_pedido = navegador.find_element(By.XPATH, '//*[@id="formu:dtInicio_input"]')
data_inicio_pedido.clear()
data_inicio_pedido.send_keys(Sete_Dias)
time.sleep(2)

# Clicar em Carregar
navegador.find_element(By.XPATH, '//*[@id="formu:j_idt39"]/span').click()
time.sleep(60)

# Clicar em Gerar
navegador.find_element(By.XPATH, '//*[@id="formu:j_idt82"]/span').click()
time.sleep(10)

    # Função para ler o valor da célula A2
def ler_valor_celula_a2(arquivo):
        df = pd.read_excel(arquivo)
        valor_a2 = df.iloc[0, 0]  # Lê o valor da célula A2 -1
        return valor_a2
