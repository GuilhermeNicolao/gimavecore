from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from openpyxl.styles import PatternFill
from openpyxl import load_workbook
from selenium import webdriver
from tkinter import messagebox
import tkinter as tk
import pandas as pd
import pyperclip
import time
import sys
import os


def iniciar_script():
    
    global diretorio 
    global nome_arquivo

    diretorio = entry_diretorio.get()
    nome_arquivo = entry_arquivo.get()

    if not diretorio:
        messagebox.showerror("Erro", "Cole o diretório do borderô.")
        return

    if not nome_arquivo:
        messagebox.showerror("Erro", "Digite o nome do arquivo.")
        return

    root.destroy()
    executar_script(diretorio, nome_arquivo)


def executar_script(diretorio, nome_arquivo):

    # Configurar opções do Chrome
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # options.add_argument("--headless=new") # Executar em modo headless
    prefs = {
        "credentials_enable_service": False,  # Desativa o serviço de credenciais
        "profile.password_manager_enabled": False  # Desativa o gerenciador de senhas
    }
    options.add_experimental_option("prefs", prefs)

    # Inicializar navegador com as opções
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=options)

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

    #Variáveis / Diretórios / Loads
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    wb = load_workbook(caminho_arquivo)
    ws = wb["Reembolso"]

    # Abrir página
    navegador.get("http://an148124.protheus.cloudtotvs.com.br:1703/webapp/")
    WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    actions = ActionChains(navegador)

    #Logar e entrar no módulo manualmente
    time.sleep(60)

    #Outras ações
    esperar_e_clicar_simples(navegador, "COMP4606")
    time.sleep(2)

    #Bordero
    esperar_e_clicar_simples(navegador, "COMP4614")
    time.sleep(2)

    #Bordero 2
    esperar_e_clicar_simples(navegador, "COMP4615")
    time.sleep(4)


    # ------ MONTAGEM DO BORDERÔ -------------------#

    # Faz a leitura dos IDs de reembolsos na PLANILHA
    df = pd.read_excel(caminho_arquivo, sheet_name="Reembolso", engine="openpyxl")

    valores_coluna_f = df.iloc[:, 5] #F2 em diante

    valores_nao_vazios = valores_coluna_f.dropna().astype(int).apply(lambda x: f"{x:09d}")

    ids_planilha = valores_nao_vazios.tolist()

    fill_amarelo = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type = "solid") #Grifar IDs que estão no borderô

    ids_processados = set() #IDs já checados.

    while True:

        #Capturar número do bordero
        elemento = WebDriverWait(navegador, 40).until(EC.presence_of_element_located((By.ID, "COMP6018")))
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
        num_bordero = pyperclip.paste()

        # time.sleep(15) #Opção para mudar a data do borderô  

        #Banco
        inserir_Sem_Espaço(navegador,"COMP6022", "756",30)
        time.sleep(1)

        #Agencia
        inserir_Sem_Espaço(navegador,"COMP6023" ,"3337",30)
        time.sleep(1)

        #Conta
        inserir_Sem_Espaço(navegador,"COMP6024", "3780624",30)
        time.sleep(1)

        #Modelo
        inserir_Sem_Espaço(navegador,"COMP6030", "02",30)
        time.sleep(2)

        #Tipo Pagamento
        inserir_Sem_Espaço(navegador,"COMP6031" ,"20",30)
        time.sleep(1)

        #OK
        esperar_e_clicar_simples(navegador, "COMP6032")
        time.sleep(7)

        #Scroll down para localizar o filtro
        tcbrowse = navegador.find_element(By.ID, "COMP6003")
        for _ in range(10):  
            tcbrowse.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        #Selecinar o filtro
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(2)

        #Clicar no Confirmar
        esperar_e_clicar(navegador,"COMP6008")
        time.sleep(40)


        #Desmarcar todos os campos selecionados
        wa_element = navegador.find_element(By.ID, "COMP6008")
        navegador.execute_script("""
            const shadow = arguments[0].shadowRoot;
            const target = shadow.querySelector('th[id="0"]');
            if (target) {
                target.click();
            } else {
                console.error("Elemento <th id='0'> não encontrado.");
            }
        """, wa_element)

        #Acessar o campo "Reembolso"
        time.sleep(10)
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(4)
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(4)
        actions.send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(4)

        #Variáveis de controle
        bordero = 0
        encontrados_nesse_bordero = 0
        tentativas_mesmo_id = 0
        ultimo_id_lido = None

        while bordero <= 99: #Tamanho do borderô
            actions = ActionChains(navegador)
            actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

            time.sleep(0.2)  # Pequeno delay para garantir que o clipboard atualize
            copied_text = pyperclip.paste()

            #Verifica se está repetindo o mesmo ID
            if copied_text == ultimo_id_lido:
                tentativas_mesmo_id +=1
            else:
                tentativas_mesmo_id = 0 #Reinicia o contador
                ultimo_id_lido = copied_text


            #Se repetiu o mesmo ID 3 vezes, salva o borderô e finaliza o script
            if tentativas_mesmo_id >= 3:

                #Salvar
                esperar_e_clicar_simples(navegador, "COMP6013")

                # Salvar alterações Excel
                wb.save(caminho_arquivo)
                print(f"✅ Borderô gerado com {encontrados_nesse_bordero} IDs.")
                time.sleep(3)
                

                print("\n🚫 Nenhum novo ID foi encontrado. Encerrando geração de borderôs...")
                time.sleep(8)
                sys.exit()
                
            print("Reembolso Protheus:", copied_text)

            if copied_text in ids_planilha:
                ActionChains(navegador).send_keys(Keys.ENTER).perform()
                bordero +=1
                encontrados_nesse_bordero +=1
                ids_processados.add(copied_text)

                # Localiza o índice do ID copiado na lista e grifa de amarelo a célula no Excel
                index = ids_planilha.index(copied_text) 
                excel_row = index + 2  # Linha real no Excel (F2 em diante)
                ws[f"F{excel_row}"].fill = fill_amarelo
                ws[f"I{excel_row}"] = num_bordero
                print(f"Colorindo F{excel_row} de amarelo.")

                
                print("ID Encontrado. Títulos dentro do borderô no momento: ", {bordero})
                time.sleep(3)
                ActionChains(navegador).send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(3)
            else:
                ActionChains(navegador).send_keys(Keys.ARROW_DOWN).perform()
                print("ID NÃO ENCONTRADO. Prosseguindo...")
                time.sleep(3)

        #Salvar
        esperar_e_clicar_simples(navegador, "COMP6013")
        time.sleep(3)

        # Salvar alterações Excel
        wb.save(caminho_arquivo)
        time.sleep(3)

        # Verificação de fim de processamento
        if encontrados_nesse_bordero == 0:
            print("\n🚫 Nenhum novo ID foi encontrado. Encerrando geração de borderôs...")
            time.sleep(7)
            sys.exit()
        else:
            print(f"✅ Borderô gerado com {encontrados_nesse_bordero} IDs.")



root = tk.Tk()
root.title("Montagem de borderôs")
root.geometry("300x150")
root.configure(bg="gray")

label_diretorio = tk.Label(root, text="Cole aqui o diretório do borderô:", bg="gray", fg="white")
label_diretorio.pack(pady=3)
entry_diretorio = tk.Entry(root)
entry_diretorio.pack(pady=3)

label_arquivo = tk.Label(root, text="Digite o nome do arquivo:", bg="gray", fg="white")
label_arquivo.pack(pady=3)
entry_arquivo = tk.Entry(root)
entry_arquivo.pack(pady=3)

botao = tk.Button(root, text="Iniciar", command=iniciar_script, bg="darkgray", fg="white")
botao.pack(pady=10)

root.mainloop()
