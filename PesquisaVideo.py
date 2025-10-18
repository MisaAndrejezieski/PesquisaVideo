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

# Configuração de logging (registra as ações no arquivo de log)
logging.basicConfig(
    filename='automacao_video.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Lista de vídeos (URLs)
videos = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    # Adicione mais URLs aqui, se desejar
]

# Define o tempo de espera padrão (em segundos)
TEMPO_ESPERA = 5

# Ativa o modo de segurança do PyAutoGUI:
# mover o mouse para o canto superior esquerdo interrompe o script.
pyautogui.FAILSAFE = True


# ===========================================
# FUNÇÕES DE APOIO
# ===========================================

def notificar_usuario(mensagem):
    """Exibe e registra mensagens no console e no log."""
    print(mensagem)
    logging.info(mensagem)


def localizar_chrome():
    """Localiza o caminho do Google Chrome automaticamente."""
    chrome_path = shutil.which("chrome")
    if not chrome_path:
        # Caminho padrão no Windows, caso o sistema não encontre
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    return chrome_path


def abrir_chrome():
    """Abre o navegador Google Chrome."""
    try:
        chrome_path = localizar_chrome()
        subprocess.Popen([chrome_path])
        time.sleep(5)  # Aguarda o navegador abrir completamente
        notificar_usuario("Navegador Chrome aberto com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Erro ao abrir o Chrome: {e}")
        return False


def realizar_pesquisa(url):
    """Abre uma nova aba e acessa a URL informada."""
    try:
        pyautogui.hotkey('ctrl', 't')  # Abre nova aba
        time.sleep(TEMPO_ESPERA)
        pyautogui.write(url)
        pyautogui.press('enter')
        notificar_usuario(f"Acessando: {url}")
        time.sleep(10)  # Aguarda o carregamento da página

        # Tentativa de clicar no botão de play (opcional)
        # Para funcionar, salve uma imagem "play_button.png" do botão de play.
        play_button = pyautogui.locateCenterOnScreen('play_button.png', confidence=0.7)
        if play_button:
            pyautogui.click(play_button)
            notificar_usuario("Botão de play identificado e clicado.")
        else:
            # Fallback: clica no centro da tela (ajustável)
            pyautogui.click(900, 500)
            notificar_usuario("Clicado no centro da tela (play provável).")

    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")


def minimizar_navegador():
    """Minimiza todas as janelas do navegador."""
    try:
        pyautogui.hotkey('win', 'd')
        notificar_usuario("Navegador minimizado.")
    except Exception as e:
        logging.error(f"Erro ao minimizar o navegador: {e}")


def fechar_navegador():
    """Fecha todas as janelas do Chrome."""
    try:
        os.system("taskkill /IM chrome.exe /F")
        notificar_usuario("Navegador Chrome fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")


def solicitar_duracao_video():
    """Solicita ao usuário a duração do vídeo (em segundos)."""
    try:
        # Evita usar input() se o script estiver empacotado (.exe)
        if sys.stdin.isatty():
            duration_str = input('Insira a duração do vídeo em segundos (padrão 300): ')
        else:
            duration_str = ""
        return int(duration_str) if duration_str else 300
    except Exception as e:
        logging.error(f"Erro ao solicitar duração: {e}")
        return 300


# ===========================================
# EXECUÇÃO PRINCIPAL
# ===========================================

def executar_automacao(num_videos=5):
    """Executa o processo de assistir vídeos automaticamente."""
    video_duration = solicitar_duracao_video()
    notificar_usuario('Iniciando automação de visualização de vídeos...')

    # Abre o Chrome uma única vez e assiste vários vídeos
    if abrir_chrome():
        try:
            for i in range(num_videos):
                video_url = random.choice(videos)
                notificar_usuario(f"Iniciando vídeo {i+1}/{num_videos}: {video_url}")
                realizar_pesquisa(video_url)
                time.sleep(video_duration)  # Aguarda a duração simulada do vídeo
                minimizar_navegador()
                time.sleep(3)  # Pausa entre vídeos
        except pyautogui.FailSafeException:
            notificar_usuario("Automação interrompida manualmente (fail-safe).")
        except Exception as e:
            logging.error(f"Erro durante a automação: {e}")
        finally:
            fechar_navegador()
            notificar_usuario("Automação finalizada.")
    else:
        logging.error("Falha ao iniciar o Chrome.")


# ===========================================
# PONTO DE ENTRADA
# ===========================================

if __name__ == "__main__":
    executar_automacao()
