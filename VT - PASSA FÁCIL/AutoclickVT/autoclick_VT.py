import pyautogui
import time

botao_imagem = "botao_autoclick_VT.png"

intervalo = 6

try:
    while True:
       
        botao_posicao = pyautogui.locateCenterOnScreen(botao_imagem, confidence=0.8)
        
        if botao_posicao is not None:
            print(f"Botão encontrado em {botao_posicao}. Clicando...")
            pyautogui.click(botao_posicao) 
        else:
            print("Botão não encontrado. Tentando novamente...")
        
        time.sleep(intervalo)  

except KeyboardInterrupt:
    print("Script interrompido pelo usuário.")

    #
