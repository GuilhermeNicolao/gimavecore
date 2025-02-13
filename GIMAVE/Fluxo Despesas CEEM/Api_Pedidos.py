import os
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

# Configurações do Chrome para download
options = webdriver.ChromeOptions()
download_path = r"C:\Users\Guilherme.Silva\Desktop\FLUXO DESPESA CEEM"
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

# Abrir o link do portal
navegador.get("https://portaleucard.virtusinfo.com.br:8443/SGC/relatorios/contas_receber/relatorio.xhtml")

# Preencher Usuário e Senha
navegador.find_element(By.XPATH, '//*[@id="formLogin:Usuario"]').send_keys("1234567890")
navegador.find_element(By.XPATH, '//*[@id="formLogin:senha"]').send_keys("1234567890")
navegador.find_element(By.XPATH, '//*[@id="formLogin:j_idt24"]/span').click()

# Espera explícita para garantir que o elemento esteja presente
wait = WebDriverWait(navegador, 10)

def baixar_relatorio(data_inicial, data_final, nome_arquivo):
    """Função para baixar o relatório entre duas datas e renomear o arquivo baixado."""
    try:
        # Preencher a data inicial
        elemento_busca = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="j_idt24:dtInicio_input"]')))
        elemento_busca.clear()
        elemento_busca.send_keys(data_inicial)
        time.sleep(1)

        # Preencher a data final
        actions = ActionChains(navegador)
        actions.send_keys(Keys.TAB).perform()
        Data_Final = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="j_idt24:dtFinal_input"]')))
        Data_Final.clear()
        Data_Final.send_keys(data_final)
        time.sleep(2)

        # Clicar em Carregar e esperar o download
        Carregar = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="j_idt24:j_idt46"]/span'))).click()
        time.sleep(10)
        Gerar_Planilha = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="j_idt24:j_idt77"]/span'))).click()
        time.sleep(10)

        # Renomear o arquivo baixado
        old_filename = os.path.join(download_path, "Contas_Receber.xlsx")
        new_filename = os.path.join(download_path, nome_arquivo)

        # Esperar o arquivo ser criado
        while not os.path.exists(old_filename):
            time.sleep(1)

        # Remover arquivo antigo se existir
        if os.path.exists(new_filename):
            os.remove(new_filename)

        os.rename(old_filename, new_filename)
        print(f"Arquivo renomeado para: {new_filename}")

        # Ler a planilha e armazenar os dados na variável
        df = pd.read_excel(new_filename)
        
        # Converter todas as colunas de data para strings
        df = df.applymap(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, (pd.Timestamp, datetime)) else x)

        return df.values.tolist()  # Retornar dados como lista de listas

    except Exception as e:
        print("Erro ao tentar baixar o relatório:", e)

# Baixar relatórios para pedidos em aberto e pedidos que irão vencer
valores_adicionar = baixar_relatorio('07/06/2023', ontem_formatado, f"Pedidos_Aberto_{hoje.day:02d}_{hoje.month:02d}_{hoje.year}.xlsx")
time.sleep(5)
valores_adicionar_Two = baixar_relatorio( hoje_formatado, '01/12/2026', f"Pedidos_Vencer_{hoje.day:02d}_{hoje.month:02d}_{hoje.year}.xlsx")

# Acessar a página de relatórios
navegador.get("https://portaleucard.virtusinfo.com.br:8443/SGC/relatorios/pedido_diario/relatorio.xhtml")

# Preencher datas no formulário
data_inicio_pedido = navegador.find_element(By.XPATH, '//*[@id="formu:dtInicio_input"]')
data_inicio_pedido.clear()
data_inicio_pedido.send_keys(Sete_Dias)
time.sleep(2)

# Clicar em Carregar
navegador.find_element(By.XPATH, '//*[@id="formu:j_idt39"]/span').click()
time.sleep(15)

# Clicar em Gerar
navegador.find_element(By.XPATH, '//*[@id="formu:j_idt78"]/span').click()
time.sleep(10)

    # Função para ler o valor da célula A2
def ler_valor_celula_a2(arquivo):
        df = pd.read_excel(arquivo)
        valor_a2 = df.iloc[0, 0]  # Lê o valor da célula A2 -1
        return valor_a2

# Chamar a função para renomear e ler o arquivo
def renomear_e_ler_arquivo(nome_arquivo):
    old_filename = os.path.join(download_path, "Pedido_Diario.xlsx")  # Nome padrão do arquivo baixado
    new_filename = os.path.join(download_path, nome_arquivo)

    # Espera o arquivo ser criado
    while not os.path.exists(old_filename):
        time.sleep(1)

    if os.path.exists(new_filename):
        os.remove(new_filename)

    os.rename(old_filename, new_filename)
    print(f"Arquivo renomeado para: {new_filename}")

    # Ler a planilha e armazenar os dados na variável
    df = pd.read_excel(new_filename)

    # Converter todas as colunas de data para strings
    df = df.applymap(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, (pd.Timestamp, datetime)) else x)

    # Substituir valores NaN por um valor padrão (ex: 0 ou string vazia)
    df = df.fillna('')  # Substitui NaN por string vazia

    # Selecionar todas as colunas, exceto as colunas "C" e "F" (índices 2 e 5)
    dados_selecionados = df.drop(df.columns[[2, 5]], axis=1).values.tolist()  # Extraindo todas as colunas, exceto C e F

    return dados_selecionados  # Retornar dados como lista de listas


# Chamar a função para ler o relatório de pedidos diários
dados_relatorio_diario = renomear_e_ler_arquivo(f"Pedido_Diario_{hoje.day:02d}_{hoje.month:02d}_{hoje.year}.xlsx")



# Define os escopos e informações da planilha
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1MtiQY6Q_MKdlLWsk0G5krDJkBLvYiDTBGTkEa-5sAP8"
SAMPLE_RANGE_NAME_PEDIDOS = "PEDIDOS EM ABERTO!A20:N1486"
SAMPLE_RANGE_NAME_VENCER = "A VENCER!A2:N"
SAMPLE_RANGE_NAME_PEDIDOS_ABERTO = "PEDIDOS DIÁRIOS!A:O"

def authenticate():
    """Lida com o processo de autenticação para acessar a Google Sheets API."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r"C:\Users\Guilherme.Silva\Desktop\FLUXO DESPESA CEEM\Credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def clear_range(service, range_name):
    """Limpa o intervalo especificado na planilha."""
    try:
        sheet = service.spreadsheets()
        sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
        print(f"Range {range_name} cleared successfully.")
    except HttpError as err:
        print(f"Error clearing range: {err}")

def update_sheet(service, range_name, values):
    """Atualiza a planilha especificada com novos valores."""
    try:
        sheet = service.spreadsheets()
        body = {'values': values}
        sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print(f"Sheet {range_name} updated successfully.")
    except HttpError as err:
        print(f"Error updating sheet: {err}")

def main():
    """Função principal para autenticar e interagir com a Google Sheets API."""
    creds = authenticate()
    service = build("sheets", "v4", credentials=creds)

    # Limpar os intervalos antes de adicionar novos valores
    clear_range(service, SAMPLE_RANGE_NAME_PEDIDOS)
    clear_range(service, SAMPLE_RANGE_NAME_VENCER)

    # Atualiza a planilha com os novos valores
    update_sheet(service, SAMPLE_RANGE_NAME_PEDIDOS, valores_adicionar)
    update_sheet(service, SAMPLE_RANGE_NAME_VENCER, valores_adicionar_Two)

     # Chamar a função para ler o valor da célula A2
    valor_a2 = ler_valor_celula_a2(os.path.join(download_path, f"Pedido_Diario_{hoje.day:02d}_{hoje.month:02d}_{hoje.year}.xlsx"))
    print(f"Valor da célula A2: {valor_a2}")

    # Ler os dados existentes na faixa SAMPLE_RANGE_NAME_PEDIDOS_ABERTO
    result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_PEDIDOS_ABERTO).execute()
    valores_existentes = result.get('values', [])

    # Encontrar a linha onde o valor_a2 está localizado
    linha_encontrada = None
    for i, linha in enumerate(valores_existentes):
        # Convertendo para string para evitar problemas de tipo
        if str(valor_a2) in map(str, linha):
            linha_encontrada = i + 1  # +1 porque o Google Sheets é 1-indexado
            break

    # Determina o número de linhas a serem substituídas
    num_rows_to_insert = len(dados_relatorio_diario)

    if linha_encontrada is not None:
        # Define o intervalo de atualização apenas se a linha foi encontrada
        range_inserir = f"PEDIDOS DIÁRIOS!A{linha_encontrada}:O{linha_encontrada + num_rows_to_insert - 1}"

        body_inserir = {'values': dados_relatorio_diario}
        try:
            service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=range_inserir,
                valueInputOption="USER_ENTERED",
                body=body_inserir
            ).execute()
            print(f"Dados substituídos a partir da linha {linha_encontrada}.")
        except HttpError as err:
            print(f"Erro ao inserir dados: {err}")
 # Agora, vamos arrastar as fórmulas de P52340:R52340 para as próximas linhas
        range_base = "PEDIDOS DIÁRIOS!P52340:R52340"  # Onde estão as fórmulas originais
        range_destino = f"PEDIDOS DIÁRIOS!P{linha_encontrada}:R{linha_encontrada + num_rows_to_insert - 1}"  # Onde as fórmulas serão replicadas

        # Chamar a função para arrastar as fórmulas
        arrastar_formulas(service, range_base, range_destino, num_rows_to_insert)
def arrastar_formulas(service, range_base, range_destino, num_linhas):
    """
    Função para arrastar fórmulas da última linha da base (ex: P52340:R52340) para as linhas subsequentes.

    Parameters:
    - service: objeto de serviço da API Google Sheets.
    - range_base: range de onde copiar as fórmulas, ex: 'PEDIDOS DIÁRIOS!P52340:R52340'.
    - range_destino: range onde as fórmulas serão replicadas, ex: 'PEDIDOS DIÁRIOS!P{linha_inicial}:R{linha_final}'.
    - num_linhas: número de linhas para replicar as fórmulas.
    """
    try:
        # Obter as fórmulas na linha base (ex: P52340:R52340)
        result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_base, valueRenderOption='FORMULA').execute()
        formulas_base = result.get('values', [])

        if not formulas_base:
            print(f"Nenhuma fórmula encontrada em {range_base}.")
            return
        
        # Obter as fórmulas da primeira linha do intervalo base (assumindo que é uma única linha)
        formulas_iniciais = formulas_base[0]
        print(f"Fórmulas recuperadas: {formulas_iniciais}")

        # Criar a lista de fórmulas replicadas
        formulas_replicadas = []
        for i in range(num_linhas):
            linha_replicada = []
            for formula in formulas_iniciais:
                # Atualiza o número da linha na fórmula para replicar corretamente
                nova_formula = formula.replace('52340', str(52340 + i + 1))
                linha_replicada.append(nova_formula)
            formulas_replicadas.append(linha_replicada)

        # Enviar as fórmulas replicadas para a range de destino
        body = {'values': formulas_replicadas}

        # Atualizar as células no intervalo de destino
        service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range_destino,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print(f"Fórmulas arrastadas de {range_base} para {range_destino} com sucesso.")
    
    except HttpError as err:
        print(f"Erro ao arrastar fórmulas: {err}")

def arrastar_formulas(service, range_base, range_destino, num_linhas):
    """
    Função para arrastar fórmulas da última linha da base (ex: P52340:R52340) para as linhas subsequentes.

    Parameters:
    - service: objeto de serviço da API Google Sheets.
    - range_base: range de onde copiar as fórmulas, ex: 'PEDIDOS DIÁRIOS!P52340:R52340'.
    - range_destino: range onde as fórmulas serão replicadas, ex: 'PEDIDOS DIÁRIOS!P{linha_inicial}:R{linha_final}'.
    - num_linhas: número de linhas para replicar as fórmulas.
    """
    try:
        # Obter as fórmulas na linha base
        result = service.spreadsheets().values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range_base,
            valueRenderOption='FORMULA'
        ).execute()
        formulas_base = result.get('values', [])

        if not formulas_base:
            print(f"Nenhuma fórmula encontrada em {range_base}.")
            return

        # Assumir que o intervalo base contém uma única linha
        formulas_iniciais = formulas_base[0]
        print(f"Fórmulas recuperadas: {formulas_iniciais}")

        # Criar a lista de fórmulas replicadas
        formulas_replicadas = []
        base_linha = int(range_base.split('!')[1].split(':')[0][1:])  # Extrai o número da linha base

        for i in range(num_linhas):
            linha_replicada = []
            for formula in formulas_iniciais:
                nova_formula = formula
                # Encontrar e ajustar referências de linha
                nova_formula = re.sub(r'(\d+)', lambda m: str(int(m.group(1)) + i + 1), nova_formula)
                linha_replicada.append(nova_formula)
            formulas_replicadas.append(linha_replicada)

        # Enviar as fórmulas replicadas para o destino
        body = {'values': formulas_replicadas}
        service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range_destino,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print(f"Fórmulas arrastadas de {range_base} para {range_destino} com sucesso.")

    except HttpError as err:
        print(f"Erro ao arrastar fórmulas: {err}")

    # Chamar a função para arrastar as fórmulas
    arrastar_formulas(service, range_base, range_destino, num_linhas)

    for arquivo in arquivos_para_remover:
    # Lógica para remover os arquivos baixados
        arquivos_para_remover = [
        f"Pedidos_Aberto_{hoje.day:02d}_{hoje.month:02d}_{hoje.year}.xlsx",
        f"Pedidos_Vencer_{hoje.day:02d}_{hoje.month:02d}_{hoje.year}.xlsx",
        f"Pedido_Diario_{hoje.day:02d}_{hoje.month:02d}_{hoje.year}.xlsx"
    ]
        caminho_arquivo = os.path.join(download_path, arquivo)
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            print(f"Arquivo removido: {caminho_arquivo}")
        else:
            print(f"Arquivo não encontrado: {caminho_arquivo}")

# Condição para executar o programa
if __name__ == "__main__":
    main()
