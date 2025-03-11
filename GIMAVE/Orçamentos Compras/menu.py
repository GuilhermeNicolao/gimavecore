import tkinter as tk
from tkinter import messagebox
import os
import sys
import subprocess

# Função para obter o diretório onde o script está localizado
def get_script_directory():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

# Diretório do script
script_dir = get_script_directory()

def open_cadastro():
    try:
        subprocess.Popen(['python', os.path.join(script_dir, 'cadastros.py')])  # Executa o script cadastro.py
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir cadastro.py: {e}")

def open_orcamentos():
    try:
        subprocess.Popen(['python', os.path.join(script_dir, 'telaprincipal.py')])  # Executa o script telaprincipal.py
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir telaprincipal.py: {e}")

def open_validacao():
    try:
        subprocess.Popen(['python', os.path.join(script_dir, 'validacao.py')])  # Executa o script validacao.py
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir validacao.py: {e}")

def open_dash():
    try:
        subprocess.Popen(['python', os.path.join(script_dir, 'dash.py')])  # Executa o script dash.py
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir dash.py: {e}")

def exit_program():
    """Função para fechar o programa"""
    root.quit()

# Criando a tela de menu
root = tk.Tk()
root.title("Menu Principal")
root.geometry("300x350")  # Aumentei a altura da janela para dar espaço para o novo botão
root.configure(bg="#dfdfdf")

# Adicionando o título
title_label = tk.Label(root, text="ORÇAMENTOS - COMPRAS | GIMAVE", font=("Arial", 12, "bold"), bg="#dfdfdf", fg="#333333")
title_label.pack(pady=10)

# Adicionando os botões
button_orcamentos = tk.Button(root, text="ORÇAMENTOS", width=20, height=2, command=open_orcamentos, bg="#72667c", fg="white")
button_orcamentos.pack(pady=10)

button_cadastrar = tk.Button(root, text="CADASTRAR", width=20, height=2, command=open_cadastro, bg="#72667c", fg="white")
button_cadastrar.pack(pady=10)

button_validacao = tk.Button(root, text="VALIDAÇÃO", width=20, height=2, command=open_validacao, bg="#72667c", fg="white")
button_validacao.pack(pady=10)

button_dash = tk.Button(root, text="DASHBOARD", width=20, height=2, command=open_dash, bg="#72667c", fg="white")
button_dash.pack(pady=10)  # Novo botão para abrir o dash.py

# Adicionando o botão de sair
button_exit = tk.Button(root, text="Sair", width=20, height=2, command=exit_program, bg="#d9534f", fg="white")
button_exit.pack(pady=10)

# Iniciando o loop da interface
root.mainloop()
