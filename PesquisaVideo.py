import logging
import pyautogui
import time
import random
import subprocess
import os
import shutil
import sys

# ===========================================
# CONFIGURAÇÕES GERAIS
# ===========================================

logging.basicConfig(
    filename='automacao_video.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

videos = [
    'https://www.youtube.com/watch?v=H6SZuAcqeW8',
]

TEMPO_ESPERA = 5
pyautogui.FAILSAFE = True

# ===========================================
# FUNÇÕES DE APOIO
# ===========================================

def logar(mensagem, tipo="info"):
    """Exibe no console e grava no log."""
    cores = {"ok": "\033[92m", "erro": "\033[91m", "info": "\033[94m", "fim": "\033[0m"}
    print(f"{cores.get(tipo, '')}{mensagem}{cores['fim']}")
    getattr(logging, "info" if tipo != "erro" else "error")(mensagem)

def localizar_chrome():
    caminho = shutil.which("chrome")
    if not caminho:
        caminho = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    return caminho if os.path.exists(caminho) else None

def abrir_chrome():
    """Abre o Chrome e espera carregar."""
    try:
        chrome_path = localizar_chrome()
        if not chrome_path:
            raise FileNotFoundError("Chrome não encontrado.")
        subprocess.Popen([chrome_path, "--new-window", "--start-maximized"])
        time.sleep(8)  # tempo maior para carregamento total
        logar("Chrome aberto com sucesso.", "ok")
        return True
    except Exception as e:
        logging.error(f"Erro ao abrir o Chrome: {e}", exc_info=True)
        return False

def esperar_img(img, timeout=15, conf=0.8):
    """Espera até encontrar uma imagem na tela."""
    inicio = time.time()
    while time.time() - inicio < timeout:
        pos = pyautogui.locateCenterOnScreen(img, confidence=conf)
        if pos:
            return pos
        time.sleep(1)
    return None

def detectar_erro():
    """Verifica se a tela de erro do YouTube está visível."""
    erro = pyautogui.locateOnScreen('erro_macaco.png', confidence=0.8)
    return erro is not None

def realizar_pesquisa(url):
    """Abre uma nova aba e acessa o vídeo."""
    try:
        pyautogui.hotkey('ctrl', 't')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'l')  # garante foco na barra
        time.sleep(1)
        pyautogui.write(url, interval=0.05)
        pyautogui.press('enter')
        logar(f"Acessando: {url}", "info")

        # Espera o carregamento inicial
        time.sleep(10)

        # Se detectar erro do macaco → tenta recarregar até 3x
        for tentativa in range(3):
            if detectar_erro():
                logar("⚠️ Página de erro detectada. Recarregando...", "erro")
                pyautogui.hotkey('ctrl', 'r')
                time.sleep(10)
            else:
                break
        else:
            logar("❌ Erro persistente ao carregar o vídeo.", "erro")
            return False

        # Tenta localizar o botão de play
        play = esperar_img('play_button.png', timeout=12, conf=0.7)
        if play:
            pyautogui.moveTo(play, duration=random.uniform(0.4, 0.8))
            pyautogui.click()
            logar("Botão de play clicado com sucesso.", "ok")
        else:
            # Clica no centro da tela caso não ache a imagem
            w, h = pyautogui.size()
            pyautogui.click(w // 2, h // 2)
            logar("Botão de play não encontrado, clicando no centro.", "info")

        return True

    except Exception:
        logging.error("Erro ao realizar pesquisa", exc_info=True)
        return False

def minimizar():
    try:
        pyautogui.hotkey('win', 'd')
        logar("Navegador minimizado.", "info")
    except Exception:
        logging.error("Erro ao minimizar navegador", exc_info=True)

def fechar_chrome():
    try:
        os.system("taskkill /IM chrome.exe /F >nul 2>&1")
        logar("Chrome fechado com sucesso.", "ok")
    except Exception:
        logging.error("Erro ao fechar navegador", exc_info=True)

def solicitar_duracao():
    try:
        if sys.stdin.isatty():
            tempo = input("Duração do vídeo em segundos (padrão 300): ")
        else:
            tempo = ""
        return int(tempo) if tempo else 300
    except Exception:
        return 300

# ===========================================
# EXECUÇÃO PRINCIPAL
# ===========================================

def executar_automacao(num_videos=3):
    duracao = solicitar_duracao()
    logar("Iniciando automação de vídeos...", "ok")

    if abrir_chrome():
        try:
            for i in range(num_videos):
                url = random.choice(videos)
                logar(f"🎬 Iniciando vídeo {i+1}/{num_videos}", "info")

                if realizar_pesquisa(url):
                    tempo_assistir = duracao + random.randint(-5, 5)
                    logar(f"Aguardando {tempo_assistir}s de reprodução...", "info")
                    time.sleep(tempo_assistir)
                else:
                    logar("Falha ao carregar o vídeo, pulando.", "erro")

                minimizar()
                time.sleep(random.uniform(3, 6))

        except pyautogui.FailSafeException:
            logar("⚠️ Automação interrompida manualmente.", "erro")
        finally:
            fechar_chrome()
            logar("Automação concluída.", "ok")
    else:
        logar("Falha ao abrir o Chrome.", "erro")

# ===========================================
# PONTO DE ENTRADA
# ===========================================

if __name__ == "__main__":
    executar_automacao()
