import logging
import pyautogui
import time
import random
import subprocess

# Configuração de logging
logging.basicConfig(
    filename='automacao_video.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Lista de vídeos do canal (URL dos vídeos)
videos = [
    'https://www.xvideos.com/video.ummkmbaca66/cannoball_-_os_criadores'
    # Adicione mais URLs dos vídeos aqui
]

# Define o tempo de espera padrão (em segundos) entre cada ação
TEMPO_ESPERA = 5

def notificar_usuario(mensagem):
    """Exibe uma notificação ao usuário e registra a mensagem."""
    print(mensagem)
    logging.info(mensagem)

def abrir_chrome():
    """Abre o navegador Google Chrome."""
    try:
        # Usando subprocess para abrir o Chrome
        subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe'])
        time.sleep(5)  # Espera o navegador abrir
        notificar_usuario("Navegador Chrome aberto com sucesso!")
        return True
    except Exception as e:
        logging.error(f"Erro ao abrir o Chrome: {e}")
        return False

def realizar_pesquisa(url):
    """Realiza a pesquisa do vídeo no navegador."""
    try:
        pyautogui.hotkey('ctrl', 't')  # Abre uma nova aba
        time.sleep(TEMPO_ESPERA)
        pyautogui.write(url)  # Escreve a URL do vídeo
        pyautogui.press('enter')
        time.sleep(TEMPO_ESPERA)
        
        # Esperar o vídeo carregar e dar play
        time.sleep(5)
        pyautogui.click(900, 500)  # Ajuste as coordenadas se necessário para o botão de play
        notificar_usuario(f"Vídeo encontrado e iniciado: {url}")
    except Exception as e:
        logging.error(f"Erro ao realizar a pesquisa: {e}")

def minimizar_navegador():
    """Minimiza a janela do navegador."""
    pyautogui.hotkey('win', 'd')  # Minimiza todas as janelas

def fechar_navegador():
    """Fecha o navegador."""
    try:
        pyautogui.hotkey('alt', 'f4')
        notificar_usuario("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")

def solicitar_duracao_video():
    """Solicita ao usuário a duração do vídeo em segundos."""
    try:
        duration_str = input('Por favor, insira a duração do vídeo em segundos (default 300): ')
        return int(duration_str) if duration_str else 300  # Valor padrão
    except Exception as e:
        logging.error(f"Erro ao solicitar a duração do vídeo: {e}")
        return 300  # Valor padrão

def executar_automacao(num_videos=100):
    """Executa a automação para assistir vídeos no YouTube."""
    video_duration = solicitar_duracao_video()
    notificar_usuario('O código de automação para assistir vídeos no YouTube vai começar...')
    
    for _ in range(num_videos):
        if abrir_chrome():
            video_url = random.choice(videos)
            realizar_pesquisa(video_url)
            time.sleep(video_duration)
            minimizar_navegador()  # Minimiza o navegador
            time.sleep(5)  # Espera um pouco antes de fechar
            fechar_navegador()
        else:
            logging.error("Não foi possível abrir o navegador Chrome.")
            break

executar_automacao()
