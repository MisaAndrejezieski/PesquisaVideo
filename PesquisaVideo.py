import tkinter as tk
from tkinter import messagebox
import pyautogui
import subprocess
import time
import random
import shutil
import os
import tempfile

def localizar_firefox():
    """Tenta localizar o executável do Mozilla Firefox."""
    caminhos = [
        shutil.which("firefox"),
        "C:/Program Files/Mozilla Firefox/firefox.exe",
        "C:/Program Files (x86)/Mozilla Firefox/firefox.exe"
    ]
    for caminho in caminhos:
        if caminho and os.path.exists(caminho):
            return caminho
    messagebox.showerror("Erro", "Mozilla Firefox não encontrado!")
    return None

def abrir_firefox_sem_perfil():
    """Abre o Firefox em modo totalmente anônimo (sem login, sem sincronização)."""
    firefox_path = localizar_firefox()
    if not firefox_path:
        return False

    temp_profile = tempfile.mkdtemp()  # Cria pasta temporária para o perfil
    subprocess.Popen(
        [
            firefox_path,
            "-new-window",
            "-no-remote",
            "-profile", temp_profile,
            "--private-window",  # Modo anônimo
            "about:blank"
        ],
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    )
    time.sleep(5)
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

    if abrir_firefox_sem_perfil():
        for i in range(repeticoes):
            url = random.choice(urls)
            try:
                pyautogui.hotkey("ctrl", "t")
                time.sleep(1.5)
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

        os.system("taskkill /IM firefox.exe /F")
        messagebox.showinfo("Fim", "Automação finalizada.")
    else:
        messagebox.showerror("Erro", "Não foi possível abrir o Firefox.")

# ================== INTERFACE ==================

janela = tk.Tk()
janela.title("Automação de Vídeos - PyAutoGUI + Firefox (Anônimo)")
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

tk.Button(janela, text="Iniciar Automação", font=("Arial", 12, "bold"), bg="#E66000", fg="w
