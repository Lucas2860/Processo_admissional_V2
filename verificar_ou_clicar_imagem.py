import os
import cv2
import time
import pyautogui
import numpy as np

DIRETORIO_IMAGENS = r'C:\Users\userbi\Desktop\Projetos\Processo_admissional_LUCAS\IMGs'

# Função para adicionar emojis aos prints
def emoji_status(status):
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

def apenasverificar(filename, timeout=300, threshold=0.8, region=None):
    """
    Verifica a presença de uma imagem na tela usando template matching
    
    Args:
        filename (str): Nome do arquivo de imagem
        timeout (int): Tempo máximo de busca em segundos
        threshold (float): Limiar de confiança para detecção
        region (tuple, optional): Região da tela para busca (x, y, width, height)
    
    Returns:
        bool: True se a imagem foi encontrada, False se não foi encontrada no tempo limite
    """
    # Caminho completo da imagem
    imagem_path = os.path.join(DIRETORIO_IMAGENS, filename)
    
    # Verifica se a imagem existe
    if not os.path.exists(imagem_path):
        print(f"{emoji_status('erro')} Imagem não encontrada: {imagem_path}")
        return False
    
    # Carrega a imagem de template
    imagem = cv2.imread(imagem_path, cv2.IMREAD_COLOR)
    
    # Tempo de início
    start_time = time.time()
    
    # Contador de tentativas
    tentativas = 0
    
    # Loop de verificação
    while time.time() - start_time < timeout:
        # Incrementa contador de tentativas
        tentativas += 1
        
        # Captura screenshot da região especificada ou da tela inteira
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # Converte screenshot para array do OpenCV
        image_array = np.array(screenshot)
        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Realiza template matching
        result = cv2.matchTemplate(image_bgr, imagem, cv2.TM_CCOEFF_NORMED)
        
        # Verifica se a imagem foi encontrada
        if result.max() >= threshold:
            print(f"{emoji_status('sucesso')} Imagem {filename} encontrada após {tentativas} tentativas!")
            return True
        
        # Mensagem de busca
        print(f"{emoji_status('processo')} Procurando pela imagem {filename} na tela. Tentativa {tentativas}")
        
        # Pausa entre tentativas
        time.sleep(1)
    
    # Timeout
    print(f"{emoji_status('erro')} Imagem {filename} não encontrada após {timeout} segundos")
    return False

def clickimagem(filename, regiao=None, threshold=0.8):
    """
    Localiza e clica em uma imagem na tela
    
    Args:
        filename (str): Nome do arquivo de imagem
        regiao (tuple): Região específica para busca (x, y, width, height)
        threshold (float): Limiar de confiança para detecção
    
    Returns:
        bool: True se a imagem foi encontrada e clicada, False caso contrário
    """
    try:
        # Caminho completo da imagem
        imagem_path = os.path.join(DIRETORIO_IMAGENS, filename)
        
        # Verifica se a imagem existe
        if not os.path.exists(imagem_path):
            print(f"{emoji_status('erro')} Imagem não encontrada: {imagem_path}")
            return False
        
        # Carrega a imagem
        imagem = cv2.imread(imagem_path, cv2.IMREAD_COLOR)
        
        # Captura screenshot
        screenshot = pyautogui.screenshot()
        screenshot_array = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2BGR)
        
        # Se região for especificada, recorta a screenshot
        if regiao:
            x, y, w, h = regiao
            screenshot_bgr = screenshot_bgr[y:y+h, x:x+w]
        
        # Realiza template matching
        result = cv2.matchTemplate(screenshot_bgr, imagem, cv2.TM_CCOEFF_NORMED)
        
        # Encontra a localização com maior correspondência
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Verifica se a correspondência atende ao threshold
        if max_val >= threshold:
            # Ajusta a localização se uma região foi especificada
            if regiao:
                x, y, _, _ = regiao
                loc_x = max_loc[0] + x
                loc_y = max_loc[1] + y
            else:
                loc_x, loc_y = max_loc
            
            # Clica no centro da imagem encontrada
            pyautogui.click(loc_x + imagem.shape[1]//2, loc_y + imagem.shape[0]//2)
            
            print(f"{emoji_status('sucesso')} Imagem {filename} encontrada e clicada!")
            return True
        else:
            print(f"{emoji_status('processo')} Imagem {filename} não encontrada")
            return False
    
    except Exception as e:
        print(f"{emoji_status('erro')} Erro ao processar imagem {filename}: {e}")
        return False
    

#mesma copisa, os coloquei um double click no lugar do click normal.

def doubleclickimagem(filename, regiao=None, threshold=0.8):
    """
    Localiza e clica em uma imagem na tela
    
    Args:
        filename (str): Nome do arquivo de imagem
        regiao (tuple): Região específica para busca (x, y, width, height)
        threshold (float): Limiar de confiança para detecção
    
    Returns:
        bool: True se a imagem foi encontrada e clicada, False caso contrário
    """
    try:
        # Caminho completo da imagem
        imagem_path = os.path.join(DIRETORIO_IMAGENS, filename)
        
        # Verifica se a imagem existe
        if not os.path.exists(imagem_path):
            print(f"{emoji_status('erro')} Imagem não encontrada: {imagem_path}")
            return False
        
        # Carrega a imagem
        imagem = cv2.imread(imagem_path, cv2.IMREAD_COLOR)
        
        # Captura screenshot
        screenshot = pyautogui.screenshot()
        screenshot_array = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2BGR)
        
        # Se região for especificada, recorta a screenshot
        if regiao:
            x, y, w, h = regiao
            screenshot_bgr = screenshot_bgr[y:y+h, x:x+w]
        
        # Realiza template matching
        result = cv2.matchTemplate(screenshot_bgr, imagem, cv2.TM_CCOEFF_NORMED)
        
        # Encontra a localização com maior correspondência
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Verifica se a correspondência atende ao threshold
        if max_val >= threshold:
            # Ajusta a localização se uma região foi especificada
            if regiao:
                x, y, _, _ = regiao
                loc_x = max_loc[0] + x
                loc_y = max_loc[1] + y
            else:
                loc_x, loc_y = max_loc
            
            # Clica no centro da imagem encontrada
            pyautogui.doubleClick(loc_x + imagem.shape[1]//2, loc_y + imagem.shape[0]//2)
            
            print(f"{emoji_status('sucesso')} Imagem {filename} encontrada e clicada!")
            return True
        else:
            print(f"{emoji_status('processo')} Imagem {filename} não encontrada")
            return False
    
    except Exception as e:
        print(f"{emoji_status('erro')} Erro ao processar imagem {filename}: {e}")
        return False