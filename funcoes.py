import os
import time
import numpy as np
import cv2
import pyautogui

def emoji_status(status): # Função para adicionar emojis aos prints
    emojis = {
        'sucesso': '✅',
        'erro': '❌',
        'atencao': '⚠️',
        'info': 'ℹ️',
        'processo': '🔍',
        'executando': '🟢',
        'finalizado': '🔴'
    }
    return emojis.get(status, '')

# Obter o caminho absoluto do diretório do script py atual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navegar para encontrar a pasta raiz (ajuste o número de níveis conforme necessário)
def encontrar_pasta_raiz(script_dir, niveis_acima=0):
    caminho_atual = script_dir
    for _ in range(niveis_acima):
        caminho_atual = os.path.dirname(caminho_atual)
    return caminho_atual

# Definir o diretório raiz de forma dinâmica
DIRETORIO_RAIZ = encontrar_pasta_raiz(SCRIPT_DIR)

# Configurações de Caminhos Base
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_RAIZ, 'IMGs')


def apenasverificar( #
    filename: str,
    timeout: float = 300,
    threshold: float = 0.7,
    region: tuple = None   # padrão é None (tela inteira)
) -> bool:
    """
    Verifica a presença de uma imagem na tela usando template matching.

    Args:
        filename (str): Nome do arquivo de imagem.
        timeout (float): Tempo máximo de busca em segundos.
        threshold (float): Limiar de confiança para detecção.
        region (tuple, opcional): Região da tela (x, y, w, h). Se None, usa tela inteira.

    Returns:
        bool: True se a imagem foi encontrada, False caso contrário.
    """
    imagem_path = os.path.join(DIRETORIO_IMAGENS, filename)
    if not os.path.exists(imagem_path):
        print(f"{emoji_status('erro')} Imagem não encontrada: {imagem_path}")
        return False

    template = cv2.imread(imagem_path, cv2.IMREAD_COLOR)
    th, tw = template.shape[:2]

    start_time = time.time()
    tentativas = 0

    while time.time() - start_time < timeout:
        tentativas += 1

        # captura o recorte ou tela inteira
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        image_array = np.array(screenshot)
        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        ih, iw = image_bgr.shape[:2]
        # se a área capturada for menor que o template, faz fallback para tela inteira
        if ih < th or iw < tw:
            print(f"{emoji_status('alerta')} Região {region} ({iw}x{ih}) é menor que o template ({tw}x{th}).")
            print(f"{emoji_status('processo')} Fazendo screenshot da tela inteira desta vez.")
            image_bgr = cv2.cvtColor(
                np.array(pyautogui.screenshot()), 
                cv2.COLOR_RGB2BGR
            )
            # atualiza dimensões
            ih, iw = image_bgr.shape[:2]

        # agora sim faz o template matching
        result = cv2.matchTemplate(image_bgr, template, cv2.TM_CCOEFF_NORMED)
        if result.max() >= threshold:
            print(f"{emoji_status('sucesso')} Imagem {filename} encontrada após {tentativas} tentativas!")
            return True

        area = f"região {region}" if region else "tela inteira"
        print(f"{emoji_status('processo')} Procurando pela imagem {filename} ({area}), tentativa {tentativas}")
        time.sleep(1)

    print(f"{emoji_status('erro')} Imagem {filename} não encontrada após {timeout} segundos")
    return False
