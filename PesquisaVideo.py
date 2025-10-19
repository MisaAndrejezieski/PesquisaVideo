import tkinter as tk
from tkinter import messagebox
import pyautogui
import subprocess
import time
import random
import shutil
import os

# ==========================================
# FUNÇÕES DE SUPORTE
# ==========================================

def localizar_chrome():
    """Tenta localizar o executável do Google Chrome automaticamente."""
    chrome_path = shutil.which("chrome")
    if not chrome_path:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    if not os.path.exists(chrome_path):
        messagebox.showerror("Erro", "Google Chrome não encontrado!")
        return None
    return chrome_path


def abrir_chrome():
    """Abre o Chrome em uma nova janela externa."""
    chrome_path = localizar_chrome()
    if chrome_path:
        subprocess.Popen(
            [chrome_path, "--new-window"],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        )
        time.sleep(5)
        return True
    return False


def assistir_videos():
    """Executa a automação conforme o input da interface."""
    # Captura os valores da interface
    urls = texto_urls.get("1.0", tk.END).strip().split("\n")
    repeticoes = int(entry_repeticoes.get())
    duracao = int(entry_duracao.get())

    if not urls or urls == ['']:
        messagebox.showwarning("Aviso", "Insira pelo menos uma URL de vídeo.")
        return

    messagebox.showinfo("Iniciando", "Automação iniciada. Mova o mouse para o canto superior esquerdo para parar.")

    # Ativa o modo de segurança do PyAutoGUI
    pyautogui.FAILSAFE = True

    if abrir_chrome():
        for i in range(repeticoes):
            url = random.choice(urls)
            try:
                pyautogui.hotkey("ctrl", "t")  # nova aba
                time.sleep(1)
                pyautogui.hotkey("ctrl", "l")  # foco na barra
                pyautogui.write(url, interval=0.05)
                pyautogui.press("enter")
                time.sleep(8)
                pyautogui.click(900, 500)  # tenta clicar no play
                print(f"[{i+1}] Assistindo: {url}")
                time.sleep(duracao)
            except pyautogui.FailSafeException:
                messagebox.showinfo("Interrompido", "Automação parada manualmente.")
                break
            except Exception as e:
                print(f"Erro: {e}")
        os.system("taskkill /IM chrome.exe /F")
        messagebox.showinfo("Fim", "Automação finalizada.")
    else:
        messagebox.showerror("Erro", "Não foi possível abrir o Chrome.")


# ==========================================
# INTERFACE TKINTER
# ==========================================

janela = tk.Tk()
janela.title("Automação de Vídeos com PyAutoGUI")
janela.geometry("500x550")
janela.resizable(False, False)

# Título
tk.Label(janela, text="Assistir Vídeos Automaticamente", font=("Arial", 14, "bold")).pack(pady=10)

# Campo URLs
tk.Label(janela, text="Cole as URLs dos vídeos (uma por linha):", font=("Arial", 10)).pack()
texto_urls = tk.Text(janela, height=8, width=55)
texto_urls.pack(pady=5)

# Campo repetições
tk.Label(janela, text="Quantas vezes repetir:", font=("Arial", 10)).pack(pady=5)
entry_repeticoes = tk.Entry(janela, width=10)
entry_repeticoes.insert(0, "3")
entry_repeticoes.pack()

# Campo duração
tk.Label(janela, text="Duração de cada vídeo (segundos):", font=("Arial", 10)).pack(pady=5)
entry_duracao = tk.Entry(janela, width=10)
entry_duracao.insert(0, "60")
entry_duracao.pack()

# Botão iniciar
tk.Button(janela, text="Iniciar Automação", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
          width=25, command=assistir_videos).pack(pady=20)

# Instrução
tk.Label(janela, text="Dica: Mova o mouse para o canto superior esquerdo para parar.",
         font=("Arial", 8), fg="gray").pack(pady=10)

# Rodapé
tk.Label(janela, text="Criado com ❤️ usando PyAutoGUI + Tkinter", font=("Arial", 8), fg="gray").pack(side="bottom", pady=5)

janela.mainloop()
