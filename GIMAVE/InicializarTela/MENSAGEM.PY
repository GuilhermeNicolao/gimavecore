import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QCheckBox, QWidget, QDialog, QDialogButtonBox, QLabel, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QWidget,
    QHBoxLayout,
    QDialog,
    QCheckBox,
    QScrollArea,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import subprocess  # Para executar o script externo
import pyautogui
import pandas as pd
import time 
import os
import math  # Para tratar NaN
import pyperclip
import os
import psutil
import time
import pandas as pd
import signal
import datetime



class CustomDialog(QDialog):
    """
    Caixa de mensagem personalizada com fundo branco e letras pretas.
    """

    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 300)  # Ajuste de tamanho para acomodar mais resultados

        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        # Mensagem com os resultados
        label = QLabel(message)
        label.setStyleSheet("color: black; font-size: 14px;")
        label.setAlignment(Qt.AlignTop)
        layout.addWidget(label)

        # Caixa de validação
        self.checkbox = QCheckBox("Validar mensagem")
        self.checkbox.setStyleSheet("font-size: 12px; color: black;")

        btn_ok = QPushButton("OK")
        btn_ok.setStyleSheet(
            """
            background-color: #3DC1C9; 
            color: black; 
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            """
        )
        btn_ok.clicked.connect(self.accept)

        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        def is_checked(self):
            """
            Retorna se a caixa de validação está marcada.
            """
            return self.checkbox.isChecked()


class ConferenciaWindow(QMainWindow):
    """
    Janela para Conferência.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Conferência")
        self.setGeometry(150, 150, 600, 400)

        self.data_results = {}  # Dicionário para armazenar os resultados por data
        self.selected_dates = {}
        self.load_data()  # Carregar os dados ao iniciar a janela
        self.load_selected_dates()  # Carregar o estado dos checkboxes ao iniciar
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)

        layout.addWidget(self.scroll_area)

        # Botão "Salvar"
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_selected_dates)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_dates()

    def load_dates(self):
        """
        Carrega todas as datas disponíveis e adiciona botões com checkboxes.
        """
        for date in self.data_results.keys():
            self.add_data_to_ui(date)

    def add_data_to_ui(self, date):
        """
        Adiciona um botão associado a uma data específica no layout da interface.
        """
        row_layout = QHBoxLayout()

        # Botão com a data
        data_button = QPushButton(date)
        data_button.setFixedSize(150, 30)
        data_button.clicked.connect(lambda: self.show_results(date))
        row_layout.addWidget(data_button)

        # Checkbox para marcar a data
        check_box = QCheckBox("Selecionar")
        check_box.setChecked(self.selected_dates.get(date, False))  # Define o estado inicial do checkbox
        check_box.toggled.connect(lambda checked, date=date: self.update_checkbox_state(date, checked))
        row_layout.addWidget(check_box)
        
        self.scroll_layout.addLayout(row_layout)
        self.scroll_widget.adjustSize()

    def update_checkbox_state(self, date, checked):
        """
        Atualiza o estado do checkbox para a data selecionada.
        """
        self.selected_dates[date] = checked
       
    def show_results(self, date):
        """
        Exibe os resultados diretamente carregados do JSON para a data clicada.
        """
        resultados = self.data_results.get(date, [])
        # Formata os resultados no diálogo para serem exibidos
        if resultados:
            message = "\n".join(resultados)
        else:
            message = "Nenhum resultado encontrado para a data selecionada."

        dialog = CustomDialog("Resultados", message)
        dialog.exec()

    def load_data(self):
        """
        Carrega dados do JSON, se existir.
        """
        if os.path.exists("conferencia_data.json"):
            with open("conferencia_data.json", "r") as f:
                self.data_results = json.load(f)
        else:
            self.data_results = {}

    def load_selected_dates(self):
        """
        Carrega o estado dos checkboxes a partir do arquivo 'selected_dates.json'.
        """
        if os.path.exists("selected_dates.json"):
            with open("selected_dates.json", "r") as f:
                self.selected_dates = json.load(f)
        else:
            self.selected_dates = {}

    def save_selected_dates(self):
        """
        Salva os estados dos checkboxes marcados.
        """
        with open("selected_dates.json", "w") as f:
            json.dump(self.selected_dates, f)

        # Feedback visual para o usuário
        self.show_message("Dados salvos com sucesso!")

        # Minimizar a janela após salvar
        self.showMinimized()

    def closeEvent(self, event):
        """
        Substitui o evento de fechamento para minimizar a janela em vez de fechá-la.
        """
        event.ignore()  # Ignora o evento de fechamento (não fecha a janela)
        self.showMinimized()  # Minimiza a janela ao invés de fechá-la

    def show_message(self, message):
        """
        Exibe uma mensagem para o usuário.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Informação")
        msg.exec_()




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Baixas Nf")
        self.setGeometry(100, 100, 400, 400)

        self.init_ui()
        self.apply_styles()
        self.conferencia_window = ConferenciaWindow()  # Inicializa a janela de Conferência

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft)

        # Botão "Conferência"
        self.conferencia_button = QPushButton("Conferência")
        self.conferencia_button.setFixedSize(120, 40)
        self.conferencia_button.setFont(QFont("Arial", 12))
        self.conferencia_button.clicked.connect(self.show_conferencia)

        # Carregar a imagem "gimave.png"
        self.title_label = QLabel()
        pixmap = QPixmap("GimaveS.png")  # Caminho correto para a imagem
        self.title_label.setPixmap(pixmap.scaled(250, 150, Qt.AspectRatioMode.KeepAspectRatio))  # Ajusta o tamanho da imagem

        # Adicionar o botão e a imagem ao layout
        header_layout.addWidget(self.conferencia_button)
        header_layout.addWidget(self.title_label)  # A imagem ficará ao lado do botão

        # Adicionar o header_layout ao main_layout
        main_layout.addLayout(header_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.subtitle_label = QLabel("")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        font_subtitle = QFont("Arial", 14)
        self.subtitle_label.setFont(font_subtitle)
        main_layout.addWidget(self.subtitle_label)

        font_input = QFont("Arial", 14)

        self.data_label = QLabel("Preencha as Datas (Formato DD/MM/AAAA):")
        self.data_label.setAlignment(Qt.AlignCenter)
        self.data_label.setFont(font_input)

        self.data_fields = []
        for _ in range(5):
            field = QLineEdit()
            field.setPlaceholderText("DD/MM/AAAA")
            field.setFont(font_input)
            field.setFixedWidth(400)
            self.data_fields.append(field)

        self.natureza_label = QLabel("Digite a Natureza:")
        self.natureza_label.setAlignment(Qt.AlignCenter)
        self.natureza_label.setFont(font_input)

        self.natureza_field = QLineEdit()
        self.natureza_field.setPlaceholderText("Digite 10 dígitos")
        self.natureza_field.setFont(font_input)
        self.natureza_field.setFixedWidth(400)

        button_layout = QHBoxLayout()
        self.executar_button = QPushButton("Executar")
        self.executar_button.setFont(font_input)
        self.executar_button.setFixedSize(150, 50)
        self.executar_button.clicked.connect(self.on_execute)

        self.limpar_button = QPushButton("Limpar")
        self.limpar_button.setFont(font_input)
        self.limpar_button.setFixedSize(150, 50)
        self.limpar_button.clicked.connect(self.on_clear)

        button_layout.addWidget(self.executar_button)
        button_layout.addWidget(self.limpar_button)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)
        main_layout.addWidget(self.data_label)
        for field in self.data_fields:
            main_layout.addWidget(field)
        main_layout.addWidget(self.natureza_label)
        main_layout.addWidget(self.natureza_field)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def apply_styles(self):
        self.setStyleSheet("""  
            QMainWindow {
                background-color: #004E59;
            }

            QLabel {
                color: white;
                font-size: 14px;
            }

            QLineEdit {
                background-color: #3DC1C9;
                color: #003A3E;
                border: 2px solid #017479;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton {
                background-color: #3DC1C9;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #35A8AF;
            }
        """)

    def show_conferencia(self):
        """
        Exibe a janela de conferência.
        """
        self.conferencia_window.show()


    def on_execute(self):
        datas_inseridas = [field.text() for field in self.data_fields if field.text()]
        natureza = self.natureza_field.text()

        if not natureza:
            dialog = CustomDialog("Erro", "Por favor, insira a natureza antes de executar a automação.")
            dialog.exec()
            return

        if not datas_inseridas:
            dialog = CustomDialog("Erro", "Por favor, insira data para continuar.")
            dialog.exec()
            return
        
        # Usando strptime para converter string em datetime e depois formatando
        datas_inseridas = datetime.datetime.strptime(datas_inseridas[0], "%d/%m/%Y").strftime("%d/%m/%Y")

        # Saída formatada
        print(datas_inseridas)  # Exibe: '29/11/2024'

        # Atribuindo a variáveis
        data = datas_inseridas
        natureza = natureza  # Supondo que natureza já tenha sido definida em algum outro lugar

        print(natureza)
        try:
            resultados_finais = []  # Para armazenar os resultados do script

            def resultados_coluna_b_quando_a_vazia(caminho_excel, nome_aba="Sheet1"):
                """
                Retorna e printa apenas os valores da coluna B onde a coluna A está vazia.
                """
                try:
                    # Lê o arquivo Excel
                    df = pd.read_excel(caminho_excel, sheet_name=nome_aba)
                    
                    # Filtrar linhas onde a coluna A está vazia e retornar os valores da coluna B
                    valores_coluna_b = df[df.iloc[:, 0].isna()].iloc[:, 1]  # Coluna A vazia -> Coluna B
                    
                    # Verificar se há resultados
                    if not valores_coluna_b.empty:
                        print("Resultados finais:")
                        for valor in valores_coluna_b:
                            print(valor)  # Printa apenas os valores da Coluna B
                    else:
                        print("Nenhuma linha com Coluna A vazia foi encontrada.")
                
                except Exception as e:
                    print(f"Erro ao processar o arquivo: {e}")

            # Fechar Excel (caso esteja aberto)
            def fechar_excel(nome_arquivo):
                # Fechar Excel pelo nome do processo
                for proc in psutil.process_iter(['pid', 'name']):
                    if 'EXCEL.EXE' in proc.info['name']:
                        try:
                            os.kill(proc.info['pid'], signal.SIGTERM)
                        except Exception as e:
                            print(f"Erro ao fechar o Excel: {e}")

            def clicar_ao_encontrar_esquerda(imagem, tempo_maximo=60, tempo_espera=1, confidence=0.8):
                    if not os.path.isfile(imagem):
                        print(f"Arquivo '{imagem}' não encontrado. Verifique o caminho.")
                        return

                    inicio = time.time()

                    while True:
                        try:
                            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=confidence)
                            if localizacao is not None:
                                # Clica no canto esquerdo da imagem (ajuste o valor -50 conforme necessário)
                                pyautogui.click(localizacao[0] - 50, localizacao[1])
                                print(f"Clique no botão '{imagem}' realizado no canto esquerdo.")
                                break
                            
                        except Exception as e:
                            print(f"{e}")

                        if time.time() - inicio > tempo_maximo:
                            print(f"Tempo máximo de espera atingido. Imagem '{imagem}' não encontrada.")
                            break

                        time.sleep(tempo_espera)


            def clicar_ao_encontrar_esquerda(imagem, tempo_maximo=60, tempo_espera=1, confidence=0.8):
                    if not os.path.isfile(imagem):
                        print(f"Arquivo '{imagem}' não encontrado. Verifique o caminho.")
                        return

                    inicio = time.time()

                    while True:
                        try:
                            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=confidence)
                            if localizacao is not None:
                                # Clica no canto esquerdo da imagem (ajuste o valor -50 conforme necessário)
                                pyautogui.click(localizacao[0] - 50, localizacao[1])
                                print(f"Clique no botão '{imagem}' realizado no canto esquerdo.")
                                break
                            
                        except Exception as e:
                            print(f"{e}")

                        if time.time() - inicio > tempo_maximo:
                            print(f"Tempo máximo de espera atingido. Imagem '{imagem}' não encontrada.")
                            break

                        time.sleep(tempo_espera)

            def clicar_ao_encontrar(imagem, tempo_maximo=60, tempo_espera=1, confidence=0.8):
                if not os.path.isfile(imagem):
                    print(f"Arquivo '{imagem}' não encontrado. Verifique o caminho.")
                    return

                inicio = time.time()

                while True:
                    try:
                        localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=confidence)
                        if localizacao is not None:
                            pyautogui.click(localizacao)
                            print(f"Clique no botão '{imagem}' realizado.")
                            break
                        
                    except Exception as e:
                        print(f"{e}")

                    if time.time() - inicio > tempo_maximo:
                        print(f"Tempo máximo de espera atingido. Imagem '{imagem}' não encontrada.")
                        break

                    time.sleep(tempo_espera)

            # Início do Totvs entrar em função de contas a Receber
            clicar_ao_encontrar('atualizacao.png', confidence=0.8)
            clicar_ao_encontrar('atualizacao.png', confidence=0.8)
            time.sleep(7)

            clicar_ao_encontrar('pedidos.png', confidence=0.8)
            time.sleep(7)

            clicar_ao_encontrar('seta.png', confidence=0.8)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(1)

            #Clicar em Pedidos de Vendas
            clicar_ao_encontrar('pedidos_venda.png', confidence=0.8)
            time.sleep(2)

            #Colocar data
            clicar_ao_encontrar('proteus.png')
            time.sleep(1)

            pyautogui.write(data)
            pyautogui.write("06")
            time.sleep(1)

            for _ in range(1):
                pyautogui.press("Enter")
                time.sleep(2)

            clicar_ao_encontrar('confir.png', confidence=0.8)

            #Clicar em cancelar, caso apareça
            clicar_ao_encontrar('canc_pedi.png', confidence=0.8)
            time.sleep(1)

            # Início do Totvs Esperando inserir data
            clicar_ao_encontrar('dta_emissao.png', confidence=0.9)
            time.sleep(2)

            #Colocar Data 
            pyautogui.write(data)
            time.sleep(2)

            # Clicar em Avançar
            clicar_ao_encontrar('avancar.png', confidence=0.8)
            time.sleep(3)

            # Início do Totvs Esperando inserir Natureza
            clicar_ao_encontrar('espera_pedi_ven.png', confidence=0.9)
            time.sleep(2)

            #Colocar Natureza
            pyautogui.write(natureza)
            time.sleep(2)

            # Clicar em Avançar
            clicar_ao_encontrar('avancar.png', confidence=0.8)
            time.sleep(1)

            # Clicar em Faturamento
            clicar_ao_encontrar('espera_fat.png', confidence=0.8)
            time.sleep(1)

            #Clicar em ViZualizar
            clicar_ao_encontrar('vizualizar.png', confidence=0.8)
            time.sleep(1)

            #Esperando tela de Vizualizar carregar
            clicar_ao_encontrar('espe_vizual.png', confidence=0.8)
            time.sleep(1)

            #Clicar em outras Ações
            clicar_ao_encontrar('outras_visua.png', confidence=0.8)
            time.sleep(1)

            #Clicar em Traker
            clicar_ao_encontrar('traker.png', confidence=0.8)
            time.sleep(1)

            #Esperando tela 
            clicar_ao_encontrar("esp_traker.png", confidence=0.8)
            time.sleep(1)

            #Esperando tela 
            clicar_ao_encontrar("rastrear.png", confidence=0.8)
            time.sleep(5)

            #Clicar em série 
            clicar_ao_encontrar("serie.png", confidence=0.8)
            time.sleep(2)

            # Simular o atalho Ctrl+C
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(5)  # Esperar para o sistema copiar os dados
                
            # Obter os dados copiados
            Dados_Copiados = pyperclip.paste()
            print("Dados copiados:", Dados_Copiados)

            # Separar os dados no caractere "-"
            partes = Dados_Copiados.split("-")

            # Garantir que há dados após o "-"
            if len(partes) > 1:
                # Pegar a parte após o "-"
                depois_do_traco = partes[1].strip()  # Remover espaços extras
                
                # Pegar apenas os números antes do próximo espaço
                Serie_inicial = ''.join(filter(str.isdigit, depois_do_traco.split(" ")[0]))  # Extrair todos os números como string, incluindo zeros à esquerda

                # Caso precise do valor como inteiro para cálculos, use a versão convertida para inteiro
                Serie_inicial_int = int(Serie_inicial)

                print("Número inicial extraído:", Serie_inicial)


            else:
                print("Formato inválido, não foi possível encontrar '-'")

            time.sleep(5)

            #Precionar Esc para sair da tela
            pyautogui.press('Esc')
            pyautogui.press('Esc')

            #Esperando tela de Vizualizar carregar
            clicar_ao_encontrar('espe_vizual.png', confidence=0.8)
            time.sleep(1)

            #Clicar Cancelar
            clicar_ao_encontrar("cancelar_visua.png", confidence=0.8)
            time.sleep(2)

            # Clicar em Faturamento Esperar
            clicar_ao_encontrar('espera_fat.png', confidence=0.8)
            time.sleep(1)

            # Clicar na seta para ultimo cliente
            clicar_ao_encontrar('baixo.png', confidence=0.8)
            clicar_ao_encontrar('baixo.png', confidence=0.8)
            time.sleep(1)

            # Clicar em Faturamento Esperar
            clicar_ao_encontrar('espera_fat.png', confidence=0.8)
            time.sleep(1)



            # Agora Vai pegar os dados do ultimo cliente
            #Clicar em ViZualizar
            clicar_ao_encontrar('vizualizar.png', confidence=0.8)
            time.sleep(1)

            #Esperando tela de Vizualizar carregar
            clicar_ao_encontrar('espe_vizual.png', confidence=0.8)
            time.sleep(1)

            #Clicar em outras Ações
            clicar_ao_encontrar('outras_visua.png', confidence=0.8)
            time.sleep(1)

            #Clicar em Traker
            clicar_ao_encontrar('traker.png', confidence=0.8)
            time.sleep(1)

            #Esperando tela 
            clicar_ao_encontrar("esp_traker.png", confidence=0.8)
            time.sleep(1)

            #Esperando tela 
            clicar_ao_encontrar("rastrear.png", confidence=0.8)
            time.sleep(5)

            #Clicar em série 
            clicar_ao_encontrar("serie.png", confidence=0.8)
            time.sleep(3)

            # Simular o atalho Ctrl+C
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(5)  # Esperar para o sistema copiar os dados
                
            # Obter os dados copiados
            Dados_Copiados = pyperclip.paste()
            print("Dados copiados:", Dados_Copiados)

            # Separar os dados no caractere "-"
            partes = Dados_Copiados.split("-")

            # Garantir que há dados após o "-"
            if len(partes) > 1:
                # Pegar a parte após o "-"
                depois_do_traco = partes[1].strip()  # Remover espaços extras
                
                # Pegar apenas os números antes do próximo espaço
                Serie_Final = ''.join(filter(str.isdigit, depois_do_traco.split(" ")[0]))  # Extrair todos os números como string, incluindo zeros à esquerda

                # Caso precise do valor como inteiro para cálculos, use a versão convertida para inteiro
                Serie_Final_int = int(Serie_Final)

                print("Número final extraído:", Serie_Final)

                
            else:
                print("Formato inválido, não foi possível encontrar '-'")

            time.sleep(5)

            #Precionar Esc para sair da tela
            pyautogui.press('Esc')
            pyautogui.press('Esc')
            time.sleep(1)

            #Esperando tela de Vizualizar carregar
            clicar_ao_encontrar('espe_vizual.png', confidence=0.8)
            time.sleep(1)

            #Clicar Cancelar
            clicar_ao_encontrar("cancelar_visua.png", confidence=0.8)
            time.sleep(2)

            # Clicar em Faturamento Esperar
            clicar_ao_encontrar('espera_fat.png', confidence=0.8)
            time.sleep(1)

            #Precionar Esc para sair da tela
            pyautogui.press('Esc')
            pyautogui.press('Esc')

            # Fazer a conta da Quantidade de Notas Existente
            Qtt_Notas = Serie_Final_int - Serie_inicial_int
            print("Quantidade de Notas Existente:", Qtt_Notas)

            # Dividir Qtt_Notas por 10 e arredondar para o maior inteiro
            Notas_Divididas = math.ceil(Qtt_Notas / 10)
            print("Quantidade de Notas dividida por 10 (arredondado para maior):", Notas_Divididas)

            # Início do Totvs entrar em função de contas a Receber
            clicar_ao_encontrar('atualizacao.png', confidence=0.8)
            clicar_ao_encontrar('atualizacao.png', confidence=0.8)
            time.sleep(5)
            clicar_ao_encontrar('atualizacao.png', confidence=0.8)
            time.sleep(10)

            #Clicar na Seta
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)

            #Clicar en NFE
            clicar_ao_encontrar('nfe.png', confidence=0.8)
            time.sleep(5)

            #CLICAR NA SETA NOVAMENTE
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)
            clicar_ao_encontrar('seta.png', confidence=0.8)
            time.sleep(0.5)

            #Clicar en NFS-E
            clicar_ao_encontrar('nfs_e.png', confidence=0.8)

            #Colocar data
            clicar_ao_encontrar('proteus.png')
            time.sleep(1)

            pyautogui.write(data)
            pyautogui.write("06")
            time.sleep(1)

            for _ in range(1):
                pyautogui.press("Enter")
                time.sleep(2)

            #Confirmar data 
            clicar_ao_encontrar('confir.png', confidence=0.8)
            time.sleep(5)

            #Clicar em OK
            for _ in range(2):
                clicar_ao_encontrar('ok.png', confidence=0.8)
                time.sleep(0.2)
            time.sleep(5)

            #Clicar em Esperar
            clicar_ao_encontrar_esquerda('espe_nfse.png', confidence=0.8)
            time.sleep(5)

            #Precionar Tab
            pyautogui.press('TAB')
            time.sleep(0.5)

            #Precionar Tab
            pyautogui.press('TAB')
            time.sleep(0.5)

            #Inserir Data
            pyautogui.write(data)
            time.sleep(1)

            #Inserir Data
            pyautogui.write(data)
            time.sleep(1)

            #Precionar Tab
            pyautogui.write(Serie_inicial)
            time.sleep(0.5)
            pyautogui.press("TAB")

            #Inserir NFE
            pyautogui.write(Serie_Final)
            time.sleep(1)
            pyautogui.press("TAB")
            time.sleep(0.5)

            #Precionar Tabwa
            pyautogui.press('TAB')
            time.sleep(0.5)

            #Precionar Enter
            pyautogui.press('Enter')
            time.sleep(0.5)


            #Esperar Monitoramento Carregar
            clicar_ao_encontrar('monitor.png', confidence=0.8)
            time.sleep(1)

            # Inicializar uma lista para armazenar os valores da série após cada iteração
            series_resultantes = []

            # Guardar o comprimento original de Serie_inicial
            tamanho_original = len(Serie_inicial)

            # Loop para iterar Notas_Divididas vezes
            for _ in range(Notas_Divididas):
                clicar_ao_encontrar('outras_mon.png', confidence=0.8)
                time.sleep(1)

                # Clicar em transmissão
                clicar_ao_encontrar('transmissao.png', confidence=0.7)
                time.sleep(1)

                # Pressionar Tab
                pyautogui.write('013')
                time.sleep(0.5)

                pyautogui.write(str(Serie_inicial))
                time.sleep(1)

                pyautogui.press("Enter")

                Serie_inicial_Monit = str(Serie_inicial)

                # Adicionar 10 à série inicial
                Serie_inicial_int += 10

                # Verificar se o valor ultrapassa Serie_Final_int e ajustar, se necessário
                if Serie_inicial_int > Serie_Final_int:
                    Serie_inicial_int = Serie_Final_int

                # Armazenar o novo valor de Serie_inicial_int
                series_resultantes.append(Serie_inicial_int)

                # Converter o valor de volta para string e ajustar o comprimento original (incluir zeros à esquerda, se necessário)
                Serie_inicial = str(Serie_inicial_int).zfill(tamanho_original)

                # Escrever o novo valor ajustado
                pyautogui.write(Serie_inicial)
                time.sleep(1)

                Serie_Final_Monit = Serie_inicial

                clicar_ao_encontrar('ok_mon.png', confidence=0.8)
                time.sleep(5)

                clicar_ao_encontrar('esp_nfe.png', confidence=0.8)
                time.sleep(5)

                clicar_ao_encontrar('ok_new.png', confidence=0.8)
                time.sleep(8)

                clicar_ao_encontrar('outras_mon.png', confidence=0.8)
                time.sleep(1)

                clicar_ao_encontrar('monit.png', confidence=0.8)
                time.sleep(1)

                # Pressionar Tab
                pyautogui.write('013')
                time.sleep(0.5)

                # Pressionar Tab
                pyautogui.write(Serie_inicial_Monit)
                time.sleep(0.5)

                pyautogui.press("Enter")
                time.sleep(1)

                # Pressionar Tab
                pyautogui.write(Serie_Final_Monit)
                time.sleep(0.5)

                pyautogui.press("Enter")
                time.sleep(1)

                clicar_ao_encontrar('k_mon_d.png', confidence=0.8)
                time.sleep(5)

                clicar_ao_encontrar('espe_mon.png', confidence=0.8)
                time.sleep(2)

                clicar_ao_encontrar('ok_p.png', confidence=0.8)
                time.sleep(8)

                clicar_ao_encontrar('outras_mon.png', confidence=0.8)
                time.sleep(1)

                clicar_ao_encontrar('monit.png', confidence=0.8)
                time.sleep(1)

                # Pressionar Tab
                pyautogui.write('013')
                time.sleep(0.5)

                # Pressionar Tab
                pyautogui.write(Serie_inicial_Monit)
                time.sleep(0.5)

                pyautogui.press("Enter")
                time.sleep(1)

                # Pressionar Tab
                pyautogui.write(Serie_Final_Monit)
                time.sleep(0.5)

                pyautogui.press("Enter")
                time.sleep(1)

                clicar_ao_encontrar('k_mon_d.png', confidence=0.8)
                time.sleep(5)

                clicar_ao_encontrar('espe_mon.png', confidence=0.8)
                time.sleep(2)

                clicar_ao_encontrar('ok_p.png', confidence=0.8)
                time.sleep(5)

            clicar_ao_encontrar('outras_mon.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('impri_brow.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('planilha.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('tipo_plan.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('tabela.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('servidor.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('local.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('impirmir.png', confidence=0.8)
            time.sleep(1)

            clicar_ao_encontrar('pesquisa.png', confidence=0.8)
            time.sleep(1)  # Pequena pausa entre os cliques

            for _ in range(11):
                pyautogui.press("Backspace")
                time.sleep(0.2)

            pyautogui.write(r"C:\NFE TOTVS")
            time.sleep(1)

            pyautogui.press("Enter")
            time.sleep(1)

            clicar_ao_encontrar('abrir.png', confidence=0.8)
            time.sleep(2)

            clicar_ao_encontrar('sim.png', confidence=0.8)
            time.sleep(60)

            # Caminho do arquivo Excel
            caminho_excel = "fisa022.xlsx"

            # Fechar Excel antes de ler o arquivo
            fechar_excel(caminho_excel)

            # Nome da aba (ajuste conforme necessário)
            nome_aba = "Listagem do Browse"

            # Executar a função
            resultados = resultados_coluna_b_quando_a_vazia(caminho_excel, nome_aba)

            # Exibir os resultados
            if resultados is not None:
                mensagem_resultados = "<b>Resultados finais:</b><br>" + "<br>".join(str(r) for r in resultados)
            else:
                mensagem_resultados = "Nenhum resultado foi encontrado."

            # Exibir os resultados na interface
            dialog = CustomDialog("Resultados", mensagem_resultados)
            dialog.exec()

        except subprocess.CalledProcessError as e:
            dialog = CustomDialog("Erro", f"Erro ao executar a automação: {e}")
            dialog.exec()
            

    def on_clear(self):
        for field in self.data_fields:
            field.clear()
        self.natureza_field.clear()

# Execução principal da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())