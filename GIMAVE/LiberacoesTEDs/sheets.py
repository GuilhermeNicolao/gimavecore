import requests

url = "https://script.google.com/a/macros/angelscapital.com.br/s/AKfycbyxvZBaE5Ug0jmBCAZ_ym7NdSWwO5Q3AcIPPScGt5TfdYCUJsSW_VMt_RUDQqiHoM_Ang/exec"

def ler_celula(cell):
    params = {"action": "read", "cell": cell}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("value", None)
    else:
        print(f"Erro ao ler a célula {cell}: {response.status_code} - {response.text}")
        return None



def escrever_celula(cell, value):
    params = {"action": "write", "cell": cell, "value": value}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"{value}' célula {cell}")
    else:
        print(f"Erro ao escrever na célula {cell}: {response.status_code} - {response.text}")



try:
    row = int(input("Informe a célula inicial: "))
except ValueError:
    print("Valor inválido. Por favor, insira um número inteiro.")
    exit()


while True:
    cell_h = f"H{row}"  
    value_h = ler_celula(cell_h)  
    
    if not value_h:  
        print(f"Célula {cell_h} está vazia. Parando o loop.")
        break
    
    if value_h == "PROCESSANDO":
        cell_c = f"C{row}"  
        value_c = ler_celula(cell_c)  
        print(f"{cell_h}, {value_c}")

        escrever_celula(cell_h, "LIBERADO")

    if row == 5:
        break

    row += 1  