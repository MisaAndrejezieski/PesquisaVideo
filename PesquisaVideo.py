import time
import pyautogui
import random
import logging
import requests

# Configuração de logging
logging.basicConfig(
    filename='automacao_video.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8')

# Lista de vídeos do canal (URL dos vídeos)
videos = [
    'https://youtu.be/Ed8OnrNFWe0'
    # Adicione mais URLs dos vídeos aqui
]

# Define o tempo de espera padrão (em segundos) entre cada ação
TEMPO_ESPERA = 5

def notificar_usuario(mensagem):
    print(mensagem)
    logging.info(mensagem)
    pyautogui.alert(text=mensagem, title='Notificação', timeout=2)  # Notificação sem necessidade de confirmação

def trocar_ip():
    try:
        # Substitua pelo seu código de troca de IP, como usar uma API de proxy
        # ou um serviço VPN.
        # ...
        notificar_usuario(f"IP trocado com sucesso!")
        return True
    except Exception as e:
        logging.error(f"Erro ao trocar IP: {e}")
        return False

def abrir_chrome():
    try:
        # Abre o navegador Chrome
        pyautogui.press('win')
        pyautogui.write('Google Chrome')
        pyautogui.press('enter')
        time.sleep(5)  # Espera o navegador abrir
        notificar_usuario("Navegador Chrome aberto com sucesso!")
        return True
    except Exception as e:
        logging.error(f"Erro ao abrir o Chrome: {e}")
        return False

def realizar_pesquisa(url):
    try:
        pyautogui.hotkey('ctrl', 't')  # Abre uma nova aba
        time.sleep(TEMPO_ESPERA)
        pyautogui.write(url)  # Escreve a URL do vídeo
        pyautogui.press('enter')
        time.sleep(TEMPO_ESPERA)
        # Dá play no vídeo com o atalho 'k'
        # pyautogui.press('k')
        # notificar_usuario(f"Vídeo encontrado e iniciado: {url}")
    # except Exception as e:
        # logging.error(f"Erro ao realizar a pesquisa: {e}")

def limpar_dados_navegacao():
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        notificar_usuario("Dados de navegação e cookies limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")

def fechar_navegador():
    try:
        pyautogui.hotkey('alt', 'f4')
        notificar_usuario("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")

def verificar_conectividade():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            notificar_usuario("Conectividade com a internet verificada.")
            return True
        else:
            logging.error("Falha na verificação de conectividade com a internet.")
            return False
    except requests.ConnectionError as e:
        logging.error(f"Erro ao verificar a conectividade com a internet: {e}")
        return False

def solicitar_duracao_video():
    try:
        duration_str = pyautogui.prompt(text='Por favor, insira a duração do vídeo em segundos:', title='Duração do Vídeo', default='300')
        return int(duration_str)
    except Exception as e:
        logging.error(f"Erro ao solicitar a duração do vídeo: {e}")
        return 300  # Valor padrão

def executar_automacao(num_videos=100):
    video_duration = solicitar_duracao_video()
    while True:
        notificar_usuario('O código de automação para assistir vídeos no YouTube vai começar...')
        if verificar_conectividade():
            for _ in range(num_videos):
                if trocar_ip():
                    if abrir_chrome():
                        video_url = random.choice(videos)
                        realizar_pesquisa(video_url)
                        time.sleep(video_duration)
                        fechar_navegador()
                        limpar_dados_navegacao()
                    else:
                        logging.error("Não foi possível abrir o navegador Chrome.")
                else:
                    logging.error("Não foi possível trocar o IP.")
        else:
            notificar_usuario("Não foi possível verificar a conectividade com a internet.")
        break

executar_automacao()

