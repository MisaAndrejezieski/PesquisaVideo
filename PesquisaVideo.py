import tkinter as tk
from tkinter import messagebox
import pyautogui
import subprocess
import time
import random
import shutil
import os

def localizar_chrome():
    """Tenta localizar o executável do Google Chrome."""
    chrome_path = shutil.which("chrome")
    if not chrome_path:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    if not os.path.exists(chrome_path):
        messagebox.showerror("Erro", "Google Chrome não encontrado!")
        return None
    return chrome_path

def abrir_chrome_com_perfil():
    """Abre o Chrome com o perfil do usuário padrão (evita erro do macaco)."""
    chrome_path = localizar_chrome()
    if not chrome_path:
        return False

    # Caminho padrão do perfil do Chrome no Windows
    user_data_dir = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    subprocess.Popen(
        [
            chrome_path,
            "--new-window",
            "--user-data-dir=" + user_data_dir,
            "--profile-directory=Default",
            "about:blank"
        ],
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    )
    time.sleep(6)
    return True

def assistir_videos():
    urls = texto_urls.get("1.0", tk.END).strip().split("\n")
    repeticoes = int(entry_repeticoes.get())
    duracao = int(entry_duracao.get())

    if not urls or urls == ['']:
        messagebox.showwarning("Aviso", "Insira pelo menos uma URL de vídeo.")
        return

    messagebox.showinfo("Iniciando", "Automação iniciada. Mova o mouse para o canto superior esquerdo para parar.")
    pyautogui.FAILSAFE = True

    if abrir_chrome_com_perfil():
        for i in range(repeticoes):
            url = random.choice(urls)
            try:
                pyautogui.hotkey("ctrl", "t")
                time.sleep(1.2)
                pyautogui.hotkey("ctrl", "l")
                pyautogui.typewrite(url, interval=0.05)
                pyautogui.press("enter")

                time.sleep(6)
                pyautogui.click(pyautogui.size().width // 2, pyautogui.size().height // 2)

                print(f"[{i+1}] Assistindo: {url}")
                time.sleep(duracao)
            except pyautogui.FailSafeException:
                messagebox.showinfo("Parado", "Automação interrompida manualmente.")
                break
            except Exception as e:
                print(f"Erro: {e}")

        os.system("taskkill /IM chrome.exe /F")
        messagebox.showinfo("Fim", "Automação finalizada.")
    else:
        messagebox.showerror("Erro", "Não foi possível abrir o Chrome.")

# ================== INTERFACE ==================

janela = tk.Tk()
janela.title("Automação de Vídeos com PyAutoGUI")
janela.geometry("500x550")
janela.resizable(False, False)

tk.Label(janela, text="Assistir Vídeos Automaticamente", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(janela, text="Cole as URLs dos vídeos (uma por linha):", font=("Arial", 10)).pack()
texto_urls = tk.Text(janela, height=8, width=55)
texto_urls.pack(pady=5)

tk.Label(janela, text="Quantas vezes repetir:", font=("Arial", 10)).pack(pady=5)
entry_repeticoes = tk.Entry(janela, width=10)
entry_repeticoes.insert(0, "3")
entry_repeticoes.pack()

tk.Label(janela, text="Duração de cada vídeo (segundos):", font=("Arial", 10)).pack(pady=5)
entry_duracao = tk.Entry(janela, width=10)
entry_duracao.insert(0, "60")
entry_duracao.pack()

tk.Button(janela, text="Iniciar Automação", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
          width=25, command=assistir_videos).pack(pady=20)

tk.Label(janela, text="Dica: Mova o mouse para o canto superior esquerdo para parar.",
         font=("Arial", 8), fg="gray").pack(pady=10)

tk.Label(janela, text="Criado com ❤️ usando PyAutoGUI + Tkinter",
         font=("Arial", 8), fg="gray").pack(side="bottom", pady=5)

janela.mainloop()
