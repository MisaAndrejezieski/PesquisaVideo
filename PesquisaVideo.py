import logging
import pyautogui
import requests
import time
import random

# Configuração de logging
logging.basicConfig(
    filename='automacao_video.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Lista de vídeos do canal (URL dos vídeos)
videos = [
    'https://www.youtube.com/shorts/yRMN-ymQReE'
    # Adicione mais URLs dos vídeos aqui
]

# Lista de proxies
proxy_list = [
    'http://103.191.218.153:8080',
    'http://85.117.56.151:8080',
    'http://103.155.246.180:8081',
    'http://103.76.149.198:8082',
    'http://103.230.49.132:8080',
    'http://157.20.157.4:8080',
    'http://51.255.20.138:80',
    'http://103.127.1.130:80',
    'http://113.160.132.195:8080',
    'http://31.210.50.227:8081',
    'http://179.104.70.12:8080',
    'http://14.177.236.212:55443',
    'http://200.49.242.18:8080',
    'http://177.93.60.70:999',
    'http://101.109.50.148:8080',
    'http://148.72.165.7:30127',
    'http://72.10.160.91:8167',
    'http://34.100.189.30:8561',
    'http://94.19.0.131:80',
    'http://47.88.59.79:82',
    'http://147.139.208.214:8080'
]

# Define o tempo de espera padrão (em segundos) entre cada ação
TEMPO_ESPERA = 5

def notificar_usuario(mensagem):
    """Exibe uma notificação ao usuário e registra a mensagem."""
    print(mensagem)
    logging.info(mensagem)
    pyautogui.alert(text=mensagem, title='Notificação', timeout=2)

def trocar_ip():
    """Troca o IP usando um serviço de proxy."""
    try:
        proxy = random.choice(proxy_list)
        
        proxies = {
            'http': proxy,
            'https': proxy
        }
        
        response = requests.get('https://www.google.com', proxies=proxies)
        if response.status_code == 200:
            notificar_usuario(f"IP trocado com sucesso! Usando proxy: {proxy}")
            return True
        else:
            logging.error("Falha ao trocar o IP usando proxy.")
            return False
    except Exception as e:
        logging.error(f"Erro ao trocar IP: {e}")
        return False

def abrir_chrome():
    """Abre o navegador Google Chrome."""
    try:
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
    """Realiza a pesquisa do vídeo no YouTube."""
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

def limpar_dados_navegacao():
    """Limpa os dados de navegação e cookies do navegador."""
    try:
        pyautogui.hotkey('ctrl', 'shift', 'delete')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        notificar_usuario("Dados de navegação e cookies limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar os dados de navegação: {e}")

def fechar_navegador():
    """Fecha o navegador."""
    try:
        pyautogui.hotkey('alt', 'f4')
        notificar_usuario("Navegador fechado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao fechar o navegador: {e}")

def verificar_conectividade():
    """Verifica a conectividade com a internet."""
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
    """Solicita ao usuário a duração do vídeo em segundos."""
    try:
        duration_str = pyautogui.prompt(text='Por favor, insira a duração do vídeo em segundos:', title='Duração do Vídeo', default='300')
        return int(duration_str)
    except Exception as e:
        logging.error(f"Erro ao solicitar a duração do vídeo: {e}")
        return 300  # Valor padrão

def executar_automacao(num_videos=100):
    """Executa a automação para assistir vídeos no YouTube."""
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
