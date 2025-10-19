import pyautogui
import time
import random
import subprocess
import shutil
import os
import logging

# ===========================================
# CONFIGURAÇÃO DE LOG
# ===========================================
logging.basicConfig(
    filename='automacao_youtube.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# PyAutoGUI: modo de segurança
pyautogui.FAILSAFE = True

# ===========================================
# FUNÇÕES DE APOIO
# ===========================================

def logar(msg, tipo="info"):
    """Mostra mensagem colorida e salva no log."""
    cores = {"ok": "\033[92m", "erro": "\033[91m", "info": "\033[94m", "fim": "\033[0m"}
    print(f"{cores.get(tipo, '')}{msg}{cores['fim']}")
    getattr(logging, "info" if tipo != "erro" else "error")(msg)

def localizar_chrome():
    """Encontra o executável do Chrome."""
    caminho = shutil.which("chrome")
    if not caminho:
        caminho = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    return caminho if os.path.exists(caminho) else None

def abrir_chrome():
    """Abre o Chrome e espera inicializar."""
    chrome_path = localizar_chrome()
    if not chrome_path:
        logar("Chrome não encontrado.", "erro")
        return False
    subprocess.Popen([chrome_path, "--new-window", "--start-maximized"])
    time.sleep(7)
    logar("Chrome aberto com sucesso.", "ok")
    return True

def esperar_imagem(img, timeout=15, conf=0.8):
    """Espera até encontrar uma imagem na tela (ex: botão play)."""
    inicio = time.time()
    while time.time() - inicio < timeout:
        pos = pyautogui.locateCenterOnScreen(img, confidence=conf)
        if pos:
            return pos
        time.sleep(1)
    return None

def abrir_video(url):
    """Abre uma nova aba e acessa o vídeo."""
    pyautogui.hotkey('ctrl', 't')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    pyautogui.write(url, interval=0.05)
    pyautogui.press('enter')
    logar(f"Abrindo vídeo: {url}", "info")
    time.sleep(8)

    # Tenta clicar no play
    play = esperar_imagem('play_button.png', timeout=10, conf=0.7)
    if play:
        pyautogui.moveTo(play, duration=random.uniform(0.4, 0.8))
        pyautogui.click()
        logar("▶️ Play clicado com sucesso.", "ok")
    else:
        w, h = pyautogui.size()
        pyautogui.click(w // 2, h // 2)
        logar("Play não encontrado, clicando no centro.", "info")

def fechar_chrome():
    """Fecha todas as janelas do Chrome."""
    os.system("taskkill /IM chrome.exe /F >nul 2>&1")
    logar("Chrome fechado.", "ok")

# ===========================================
# EXECUÇÃO PRINCIPAL
# ===========================================

def executar():
    logar("=== Automação de vídeos YouTube ===", "ok")

    # Solicita URLs
    urls_input = input("Digite as URLs dos vídeos (separe por vírgula): ").strip()
    videos = [u.strip() for u in urls_input.split(",") if u.strip()]

    if not videos:
        logar("Nenhum vídeo informado. Encerrando.", "erro")
        return

    # Solicita quantas vezes iniciar
    try:
        repeticoes = int(input("Quantas vezes deseja iniciar cada vídeo? "))
        duracao = int(input("Tempo de reprodução de cada vídeo (segundos): "))
    except ValueError:
        logar("Entrada inválida. Encerrando.", "erro")
        return

    if not abrir_chrome():
        logar("Falha ao abrir Chrome.", "erro")
        return

    try:
        for r in range(repeticoes):
            logar(f"=== Rodada {r+1}/{repeticoes} ===", "info")
            for url in videos:
                abrir_video(url)
                tempo = duracao + random.randint(-5, 5)
                logar(f"Aguardando {tempo}s assistindo o vídeo...", "info")
                time.sleep(tempo)
                pyautogui.hotkey('ctrl', 'w')  # fecha aba
                time.sleep(random.uniform(2, 4))
    except pyautogui.FailSafeException:
        logar("⚠️ Automação interrompida manualmente.", "erro")
    finally:
        fechar_chrome()
        logar("Automação finalizada.", "ok")

# ===========================================
# PONTO DE ENTRADA
# ===========================================

if __name__ == "__main__":
    executar()
