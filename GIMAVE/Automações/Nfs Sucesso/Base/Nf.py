from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QLabel,
    QWidget,
    QMessageBox,
    QComboBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
import os
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import shutil
from datetime import datetime
import re
import zipfile


# Obter datas necessárias
hoje = datetime.now()
hoje_formatado = f"{hoje.year}{hoje.month:02d}{hoje.day:02d}"

# Caminho para o arquivo Excel
EXCEL_BASE =  r'\\172.32.2.77\e\DADOS\NF_Sucesso\dist\base.xlsx'

# Função para ler dados da planilha Excel
def get_sheet_data_excel(caminho_planilha):
    try:
        # Lê a planilha Excel
        df = pd.read_excel(caminho_planilha)
        # Filtra as colunas relevantes (Razão Social e CNPJ)
        df = df[['Razão social', 'CNPJ']]
        return df
    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Erro ao acessar a planilha: {e}")
        return None

# Função para formatar o CNPJ no formato "00.000.000/0000-00"
def formatar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))  # Remove qualquer caracter não numérico
    if len(cnpj) == 14:  # Verifica se é um CNPJ válido
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj  # Retorna sem formatação se não for um CNPJ válido

# Função para buscar o CNPJ pela nome da empresa
def buscar_cnpj_empresa(nome_empresa, cnpj_input, client_name_input):
    dados_planilha = get_sheet_data_excel(EXCEL_BASE)
    
    if dados_planilha is None or dados_planilha.empty:
        QMessageBox.information(None, "Resultado", "Não foi possível obter dados da planilha.")
        return
    
    # Busca o nome da empresa na planilha
    cnpj_encontrado = None
    for _, linha in dados_planilha.iterrows():
        nome_na_planilha = linha['Razão social'].strip().lower()
        cnpj = linha['CNPJ'].strip()

        if nome_empresa.lower() in nome_na_planilha:
            cnpj_encontrado = cnpj
            break

    if cnpj_encontrado:
        cnpj_formatado = formatar_cnpj(cnpj_encontrado)
        cnpj_input.setText(cnpj_formatado)  # Preenche o campo CNPJ
        client_name_input.setText(nome_empresa)  # Preenche o campo Nome do Cliente
    else:
        QMessageBox.information(None, "Resultado", f"Nenhum CNPJ encontrado para a empresa '{nome_empresa}'.")



# Caminho para o arquivo Excel
EXCEL_FILE = r"\\172.32.2.77\e\DADOS\NF_Sucesso\dist\user_data.xlsx"

class SignUpForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Usuário")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("QMainWindow { background-color: #0B002C; }")

        # Configuração do layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(r"\\172.32.2.77\e\DADOS\NF_Sucesso\dist\nf.png").scaled(200, 200, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Campo de Nome
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nome")
        self.username_input.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.username_input)

        # Campo de Senha
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.password_input)

        # Campo de Confirmação de Senha
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar Senha")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.confirm_password_input)

        # Checkbox para aceitar os termos
        self.terms_checkbox = QCheckBox("Aceitar os Termos")
        self.terms_checkbox.setStyleSheet("QCheckBox { color: white; }")
        main_layout.addWidget(self.terms_checkbox)

        # Botão de Cadastro
        register_button = QPushButton("Cadastrar")
        register_button.setStyleSheet(self.get_button_style())
        register_button.clicked.connect(self.register_user)
        main_layout.addWidget(register_button)

        # Botão de Login
        login_label = QPushButton("Já tem Cadastro? Entrar")
        login_label.setStyleSheet(
            "QPushButton { color: #55aaff; background: none; border: none; font-size: 14px; margin: 10px 0; }"
        )
        login_label.clicked.connect(self.show_login_form)
        main_layout.addWidget(login_label)

        self.setCentralWidget(main_widget)

    def get_input_style(self):
        return """
        QLineEdit {
            border: 1px solid #555;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            background-color: #12003E;
            color: white;
        }
        QLineEdit:focus {
            border: 1px solid #55aaff;
        }
        """

    def get_button_style(self):
        return """
        QPushButton {
            background-color: #512DA8;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        QPushButton:hover {
            background-color: #673AB7;
        }
        QPushButton:pressed {
            background-color: #311B92;
        }
        """

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        agreed_terms = self.terms_checkbox.isChecked()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return

        if not agreed_terms:
            QMessageBox.warning(self, "Erro", "Você deve aceitar os termos!")
            return

        if os.path.exists(EXCEL_FILE):
            data = pd.read_excel(EXCEL_FILE)
        else:
            data = pd.DataFrame(columns=["Username", "Password"])

        if username in data["Username"].values:
            QMessageBox.warning(self, "Erro", "Usuário já cadastrado!")
            return

        new_user = {"Username": username, "Password": password}
        data = pd.concat([data, pd.DataFrame([new_user])], ignore_index=True)
        data.to_excel(EXCEL_FILE, index=False)

        QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso!")

    def show_login_form(self):
        self.login_form = LoginForm()
        self.login_form.show()
        self.close()  # Fecha a janela atual (cadastro)


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("QMainWindow { background-color: #0B002C; }")

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Ajuste do espaçamento entre os widgets
        main_layout.setSpacing(5)  # Define um espaçamento menor entre os widgets
        main_layout.setContentsMargins(10, 10, 10, 10)  # Ajuste as margens internas, se necessário

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(r"\\172.32.2.77\e\DADOS\NF_Sucesso\dist\gimave_sem fundo.png").scaled(200, 200, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        caption_label = QLabel(" Gimave ")
        caption_label.setAlignment(Qt.AlignCenter)
        caption_label.setStyleSheet(
            "color: white; font-size: 50px; font-weight: bold;"
        )
        main_layout.addWidget(caption_label)

        # Campo de Nome
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nome")
        self.username_input.setStyleSheet(SignUpForm.get_input_style(self))
        main_layout.addWidget(self.username_input)

        # Campo de Senha
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(SignUpForm.get_input_style(self))
        main_layout.addWidget(self.password_input)

        # Botão de Login
        login_button = QPushButton("Login")
        login_button.setStyleSheet(SignUpForm.get_button_style(self))
        login_button.clicked.connect(self.login_user)
        main_layout.addWidget(login_button)

        # Botão de Voltar para a tela de Cadastro
        back_button = QPushButton("Voltar para Cadastro")
        back_button.setStyleSheet(SignUpForm.get_button_style(self))
        back_button.clicked.connect(self.voltar_para_cadastro)
        main_layout.addWidget(back_button)

        self.setCentralWidget(main_widget)

    def login_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        if not os.path.exists(EXCEL_FILE):
            QMessageBox.warning(self, "Erro", "Nenhum usuário cadastrado!")
            return

        data = pd.read_excel(EXCEL_FILE)

        if username in data["Username"].values:
            user_data = data[data["Username"] == username]
            if user_data.iloc[0]["Password"] == password:
                self.show_dashboard()
            else:
                QMessageBox.warning(self, "Erro", "Senha incorreta!")
        else:
            QMessageBox.warning(self, "Erro", "Usuário não encontrado!")

    def voltar_para_cadastro(self):
        self.signup_form = SignUpForm()  # Cria uma nova instância da tela de cadastro
        self.signup_form.show()          # Exibe a tela de cadastro
        self.close()                     # Fecha a tela de login atual

    def show_dashboard(self):
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()

# Classe Dashboard
class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NF Automatica")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("QMainWindow { background-color: #0B002C; }")

        # Principal do contêiner
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Adiciona a imagem e o texto no topo
        header_label = QLabel()
        pixmap = QPixmap("/mnt/data/image.png")  # Substitua pelo caminho correto da imagem
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
        header_label.setPixmap(pixmap)
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(r"\\172.32.2.77\e\DADOS\NF_Sucesso\dist\robo.png").scaled(200, 200, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        caption_label = QLabel("Baixas NF Automáticas")
        caption_label.setAlignment(Qt.AlignCenter)
        caption_label.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold;"
        )
        main_layout.addWidget(caption_label)

        def formatar_documento(texto):
            """
            Formata automaticamente um CPF ou CNPJ baseado no comprimento da entrada.
            - CPF: 000.000.000-00
            - CNPJ: 00.000.000/0000-00
            """
            texto = ''.join(filter(str.isdigit, texto))  # Remove caracteres não numéricos

            if len(texto) == 11:  # CPF
                return f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}"
            elif len(texto) == 14:  # CNPJ
                return f"{texto[:2]}.{texto[2:5]}.{texto[5:8]}/{texto[8:12]}-{texto[12:]}"
            
            return texto  # Mantém entrada parcial sem formatar forçadamente


        # Campo de CPF/CNPJ
        self.cnpj_input = QLineEdit()
        self.cnpj_input.setPlaceholderText("Digite CPF ou CNPJ")
        self.cnpj_input.setStyleSheet(self.get_input_style())

        # Removemos o setValidator para permitir CPF e CNPJ dinâmicos
        self.cnpj_input.textChanged.connect(lambda: self.cnpj_input.setText(formatar_documento(self.cnpj_input.text())))

        main_layout.addWidget(self.cnpj_input)


        # Campo de Valor
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Valor")
        self.value_input.setStyleSheet(self.get_input_style())
        self.value_input.textChanged.connect(self.format_currency)
        main_layout.addWidget(self.value_input)

        # Campo Nome do Cliente
        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Nome do Cliente")
        self.client_name_input.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.client_name_input)

        # Campo de Período
        # Campo de Data
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("DD/MM/AAAA")  # Placeholder com formato de data
        self.data_input.setStyleSheet(self.get_input_style())
        main_layout.addWidget(self.data_input)


        # Criação de botões e layout
        button_layout = QVBoxLayout()
        baixar_drive_button = QPushButton("Baixar No Drive")
        baixar_drive_button.setStyleSheet(self.get_black_button_style())
        button_layout.addWidget(baixar_drive_button)

        self.add_button(button_layout, "Salvar NF")

        # Botão "Buscar CNPJ no SGC"
        buscar_cnpj_button = QPushButton("Buscar CNPJ no SGC")
        buscar_cnpj_button.setStyleSheet(self.get_yellow_button_style())
        buscar_cnpj_button.clicked.connect(self.buscar_cnpj_sgc)  # Certifique-se de que está chamando a função correta
        button_layout.addWidget(buscar_cnpj_button)


        executar_button = QPushButton("Executar Automoção")
        executar_button.setStyleSheet(self.get_blue_button_style())
        executar_button.clicked.connect(self.executar_automacao)  # Conectar a função
        button_layout.addWidget(executar_button)        

        # Botão "Ler Informações"
        buscar_nf_button = QPushButton("Ler Informações")
        buscar_nf_button.setStyleSheet(self.get_green_button_style())
        buscar_nf_button.clicked.connect(self.buscar_nf)
        button_layout.addWidget(buscar_nf_button)

         # Voltar e Refazer
        navigation_layout = QHBoxLayout()
        voltar_button = QPushButton("Voltar")
        voltar_button.setStyleSheet(self.get_button_style())
        voltar_button.clicked.connect(self.voltar_para_login)
        navigation_layout.addWidget(voltar_button)

        # Botão "Refazer"
        refazer_button = QPushButton("Limpar Dados")
        refazer_button.setStyleSheet(self.get_red_button_style())
        refazer_button.clicked.connect(self.refazer_campos)
        navigation_layout.addWidget(refazer_button)

        button_layout.addLayout(navigation_layout)

        # Adicionando os botões ao layout principal
        main_layout.addLayout(button_layout)

        self.setCentralWidget(main_widget)

        # Variável para armazenar o nome do cliente
        self.nome_cliente = ""

    def buscar_cnpj_sgc(self):
        """Busca o CNPJ pelo nome da empresa e preenche os campos"""
        nome_cliente = self.client_name_input.text().strip()
        if nome_cliente:
            buscar_cnpj_empresa(nome_cliente, self.cnpj_input, self.client_name_input)
        else:
            QMessageBox.warning(self, "Erro", "Por favor, insira o nome da empresa para buscar o CNPJ.")

    

    def buscar_nf(self):
        """Salva os dados de CNPJ, Valor, Data e Nome do Cliente em variáveis da classe."""
        self.cnpj_salvo = self.cnpj_input.text().strip()
        self.valor_salvo = self.value_input.text().strip()
        self.data_salvo = self.data_input.text().strip()  # Variável para a data
        self.nome_cliente_salvo = self.client_name_input.text().strip()

        # Exibir mensagem de sucesso com os dados
        msg = f"""
        <b><font color="BLACK">Dados Salvos:</font></b><br><br>
        <b>CNPJ:</b> <i>{self.cnpj_salvo}</i><br>
        <b>Valor:</b> <i>{self.valor_salvo}</i><br>
        <b>Data:</b> <i>{self.data_salvo}</i><br>
        <b>Nome do Cliente:</b> <i>{self.nome_cliente_salvo}</i>
        """
        QMessageBox.information(self, "Sucesso", msg)



    def add_button(self, layout, label_text):
        button = QPushButton(label_text)
        if label_text == "Executar Automoção":
            button.setStyleSheet(self.get_blue_button_style())
        else:
            button.setStyleSheet(self.get_button_style())
        button.clicked.connect(
            lambda: QMessageBox.information(self, "Ação", f"Botão '{label_text}' clicado!")
        )
        layout.addWidget(button)

    def refazer_campos(self):
        """Limpa todos os campos, incluindo o campo N° Pedido, e apaga arquivos da pasta de gestão."""
        
        # Limpa os campos do formulário
        self.cnpj_input.clear()
        self.value_input.clear()
        self.client_name_input.clear()
        self.data_input.clear()
        self.dados_nf = None
        self.nome_cliente = ""  # Limpa o nome do cliente
        
        # Define o caminho da pasta
        pasta_gestao = r"\\172.32.2.77\e\DADOS\NF_Sucesso\Extraidos"

        # Verifica se a pasta existe antes de tentar apagar arquivos
        if os.path.exists(pasta_gestao):
            for arquivo in os.listdir(pasta_gestao):
                caminho_arquivo = os.path.join(pasta_gestao, arquivo)
                try:
                    if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                        os.unlink(caminho_arquivo)  # Remove arquivos e links simbólicos
                    elif os.path.isdir(caminho_arquivo):
                        shutil.rmtree(caminho_arquivo)  # Remove diretórios e conteúdos
                except Exception as e:
                    QMessageBox.warning(self, "Erro", f"Erro ao apagar {arquivo}: {e}")

        QMessageBox.information(self, "Refazer", "Os campos foram limpos e os arquivos foram apagados com sucesso!")

    def voltar_para_login(self):
        """Retorna para a tela de login."""
        self.login_form = LoginForm()  # Cria uma nova instância da tela de login
        self.login_form.show()  # Exibe a tela de login
        self.close()  # Fecha o painel de controle

    def format_currency(self):
        """Formata o valor no formato brasileiro de moeda: 'R$ 0.000,00'."""
        text = self.value_input.text().replace("R$", "").replace(".", "").replace(",", "").strip()
        if text.isdigit():
            text = text.zfill(3)
            integer_part = text[:-2]
            decimal_part = text[-2:]
            formatted = f"R$ {int(integer_part):,}".replace(",", ".") + "," + decimal_part
            self.value_input.setText(formatted)

    def format_cnpj(self):
        """Aplica a formatação de CNPJ ao texto inserido."""
        text = self.cnpj_input.text().replace(".", "").replace("/", "").replace("-", "")
        if text.isdigit():
            formatted = f"{text[:2]}.{text[2:5]}.{text[5:8]}/{text[8:12]}-{text[12:14]}"
            self.cnpj_input.setText(formatted)
    

    def executar_automacao(self):

        try:

            # Verifica se os dados estão armazenados
            if not hasattr(self, "cnpj_salvo") or not hasattr(self, "valor_salvo") or not hasattr(self, "data_salvo") or not hasattr(self, "nome_cliente_salvo"):
                QMessageBox.warning(self, "Erro", "Você precisa clicar em 'Ler Informações' antes de executar a automação.")

                return

            # Recupera os dados salvos
            cnpj = self.cnpj_salvo
            valor = self.valor_salvo
            print(valor)  # Verifica o valor original

            try:
                # Remover "R$" e espaços extras
                valor = str(valor).replace("R$", "").strip()
                
                # Remover pontos de separação de milhares e substituir vírgula por ponto
                valor = valor.replace(".", "").replace(",", ".")
                
                # Converter para float e formatar com duas casas decimais
                valor = f"{float(valor):.2f}".replace(".", ",")
            except ValueError:
                valor = "0,00"

            print(valor)  # Verifica o valor final

            data = self.data_salvo
            nome_cliente = self.nome_cliente_salvo

            # Exibe os valores para depuração
            print(f"Executando automação com: CNPJ={cnpj}, Valor={valor}, Período={data}, Cliente={nome_cliente}")

            # Aqui entra o código de automação com Selenium
            # Substituir onde os valores eram preenchidos manualmente para usar os valores das variáveis acima
            
            # Caminho do script Selenium (substitua pelo caminho correto)
            # Caminho para a extensão .crx
            EXTENSAO = r"\\172.32.2.77\e\DADOS\NF_Sucesso\captcha\captcha.crx"

            # Caminho para salvar downloads
            dowlond_path = r"\\172.32.2.77\e\DADOS\NF_Sucesso"


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

            IMAGEM_ALVO = r"\\172.32.2.77\e\DADOS\NF_Sucesso\dist\bot.png"
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

            def main():
                try:
                    navegador = configurar_navegador(dowlond_path, EXTENSAO)
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
                    # Verifica se a data foi preenchida
                    if self.data_salvo:
                        # Converte a data para o formato 'YYYY-MM-DD' necessário pelo campo
                        dia, mes, ano = self.data_salvo.split("/")
                        data_formatada = f"{dia}/{mes}/{ano}"

                        # Colocar Data
                        elemento = WebDriverWait(navegador, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="conteudo_66020_101_1"]/article/div[1]/aside[1]/div/div[2]/table[2]/tbody/tr/td[2]/span/input')))
                        
                        # Preencher o campo de data usando JavaScript
                        navegador.execute_script(f"arguments[0].value = '{data_formatada}';", elemento)
                        time.sleep(1)
                    else:
                        QMessageBox.warning(self, "Erro", "Por favor, preencha a data antes de continuar.")

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
                    caminho_arquivo = esperar_download_arquivo(dowlond_path, nf_baixada)

                    if caminho_arquivo:
                        # Renomear o arquivo baixado
                        diretorio_extraidos = r"\\172.32.2.77\e\DADOS\NF_Sucesso\Extraidos"
                        nome_base = f"Cliente {nome_cliente} - CNPJ {cnpj} - VALOR {valor}.zip"
                        nome_base = re.sub(r'[^\w\s.-]', '_', nome_base)
                        caminho_destino = os.path.join(dowlond_path, nome_base + ".zip")

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

          


        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao executar a automação: {str(e)}")

    def get_input_style(self):
        return """
        QLineEdit, QComboBox {
            border: 1px solid #555;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            background-color: #12003E;
            color: white;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #9C27B0;
            background-color: #17006F;
        }
        """


    def get_button_style(self):
        return """
        QPushButton {
            background-color: #512DA8;
            color: white;
            font-size: 14px;
            padding: 8px;
            margin: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #673AB7;
        }
        QPushButton:pressed {
            background-color: #311B92;
        }
        """

    def get_green_button_style(self):
        return """
        QPushButton {
            background-color: #229A00;
            color: white;
            font-size: 14px;
            padding: 8px;
            margin: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: darkred;
        }
        QPushButton:pressed {
            background-color: maroon;
        }
        """

    def get_blue_button_style(self):
        return """
        QPushButton {
            background-color: #0000FF;
            color: white;
            font-size: 14px;
            padding: 8px;
            margin: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #1E90FF;
        }
        QPushButton:pressed {
            background-color: #00008B;
        }
        """
    
    def get_yellow_button_style(self):
        return """
        QPushButton {
            background-color: #DAA520;
            color: white;
            font-size: 14px;
            padding: 8px;
            margin: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #1E90FF;
        }
        QPushButton:pressed {
            background-color: #DAA520;
        }
        """

    def get_red_button_style(self):
        return """
        QPushButton {
            background-color: #ff0000;
            color: white;
            font-size: 14px;
            padding: 8px;
            margin: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #1E90FF;
        }
        QPushButton:pressed {
            background-color: #DAA520;
        }
        """
    
    def get_black_button_style(self):
        return """
        QPushButton {
            background-color: #000000; /* Fundo preto */
            color: white; /* Texto branco */
            font-size: 14px;
            padding: 8px;
            margin: 5px;
            border-radius: 5px;
            border: 2px solid white; /* Contorno branco com espessura 2px */
        }
        QPushButton:hover {
            background-color: #1E90FF;
            border: 2px solid #87CEFA; /* Contorno azul claro no hover */
        }
        QPushButton:pressed {
            background-color: #DAA520;
            border: 2px solid #FFD700; /* Contorno dourado no pressionamento */
        }
        """

if __name__ == "__main__":
    app = QApplication([])
    window = LoginForm()  # Troque para Dashboard
    window.show()
    app.exec()
