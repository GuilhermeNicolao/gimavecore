import pyautogui
import time

# Caminho para a imagem do botão
botao_imagem = 'botao.png'

try:
    while True:
        # Localiza a imagem na tela
        botao_localizado = pyautogui.locateOnScreen(botao_imagem, confidence=0.8)

        if botao_localizado:
            # Obtém o centro do botão para clicar
            botao_centro = pyautogui.center(botao_localizado)
            # Clica no centro do botão
            pyautogui.click(botao_centro)
            print(f"Botão clicado em {botao_centro}")
        else:
            print("Botão não encontrado. Verificando novamente...")

        # Aguarda 6 segundos antes de tentar novamente
        time.sleep(6)

except KeyboardInterrupt:
    print("Execução interrompida pelo usuário.")
