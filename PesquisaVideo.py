import tkinter as tk
from tkinter import messagebox
import pyautogui
import subprocess
import time
import random
import shutil
import os

def localizar_edge():
    """Tenta localizar o executável do Microsoft Edge."""
    edge_path = shutil.which("msedge")
    if not edge_path:
        edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    if not os.path.exists(edge_path):
        messagebox.showerror("Erro", "Microsoft Edge não encontrado!")
        return None
    return edge_path

def abrir_edge_com_perfil():
    """Abre o Edge com o perfil padrão do usuário."""
    edge_path = localizar_edge()
    if not edge_path:
        return False

    user_data_dir = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")
    subprocess.Popen(
        [
            edge_path,
            "--new-window",
            "--user-data-dir=" + user_data_dir,
            "--profile-directory=Default",
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

    if abrir_edge_com_perfil():
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

        os.system("taskkill /IM msedge.exe /F")
        messagebox.showinfo("Fim", "Automação finalizada.")
    else:
        messagebox.showerror("Erro", "Não foi possível abrir o Edge.")

# ================== INTERFACE ==================

janela = tk.Tk()
janela.title("Automação de Vídeos - PyAutoGUI + Edge")
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

tk.Button(janela, text="Iniciar Automação", font=("Arial", 12, "bold"), bg="#0078D7", fg="white",
          width=25, command=assistir_videos).pack(pady=20)

tk.Label(janela, text="Dica: Mova o mouse para o canto superior esquerdo para parar.",
         font=("Arial", 8), fg="gray").pack(pady=10)

tk.Label(janela, text="Criado com ❤️ usando PyAutoGUI + Tkinter",
         font=("Arial", 8), fg="gray").pack(side="bottom", pady=5)

janela.mainloop()
