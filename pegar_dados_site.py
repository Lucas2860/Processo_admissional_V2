import os
import pyautogui as pag
import time
import datetime
import pytesseract
from pathlib import Path
import zipfile

# Executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'R:\RPA\Publico\Livre\Tesseract-OCR\tesseract.exe'

DIRETORIO_RAIZ = r'C:\Users\userbi\Desktop\Projetos\Processo_admissional_LUCAS'
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_RAIZ, 'img')

from verificar_ou_clicar_imagem import apenasverificar,clickimagem,emoji_status


#ENTRANDO NO SITE
os.startfile("https://empresa.lugarh.com.br/documentos?Tab=Active&Order=newer&Filter=admissionStep_null&PageSize=100&PageNumber=1&QueryTerms=")#entrando site
apenasverificar('site_lugarh.png',timeout=20)#verifica se ta no site
pag.hotkey("win","up")
pag.hotkey("win","up")
time.sleep(2)
apenasverificar('site_lugarh_tela_inteira.png')

#Colocando o "itens por página" em 100
for tab in range(4):
    time.sleep(0.3)
    pag.press("tab")
for baixo in range(2):
    time.sleep(0.3)
    pag.press("down")

time.sleep(2)

#Colocando um filtro para "sem etapa" 
for tab in range(11):
    time.sleep(0.5)
    pag.press("tab")
pag.press('enter')
time.sleep(2)
clickimagem('sem_etapa.png')

time.sleep(2)
apenasverificar('selecionar_todos.png')
clickimagem('selecionar_todos.png')
time.sleep(1)
if apenasverificar('botao_de_baixar.png', timeout=3) == False:
    clickimagem('selecionar_todos.png')
apenasverificar('botao_de_baixar.png')
clickimagem('botao_de_baixar.png')
time.sleep(2)

#Exportando o documento
apenasverificar('janlea_de_esportar_documentos.png')
pag.press("tab")    
pag.press("tab")
pag.press("enter")
pag.press("tab", presses=6)
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
export_name = f"processo_admissional_{timestamp}"
pag.write(export_name)
pag.press("tab")
time.sleep(0.2)
pag.press("enter")
apenasverificar('pagina_lista_exportacao.png')

while apenasverificar("processando.png", threshold=0.9,timeout=2, region=(1304,295,140,102)) is True:
    print("Aguardando...")

apenasverificar("dowload.png")
clickimagem("dowload.png")
time.sleep(10)
pag.hotkey("win","down")
pag.hotkey("ctrl","w")

#Extraindo arquivo JSON 
def listar_downloads():
    caminho_downloads = Path.home() / "Downloads"
    if not caminho_downloads.exists():
        print("A pasta de Downloads não foi encontrada.")
        return
    arquivos_downloads = list(caminho_downloads.iterdir())
    if not arquivos_downloads:
        print("A pasta de Downloads está vazia.")
    else:
        return len(arquivos_downloads)
    
def extrair_ultimo_download_zip():
    caminho_downloads = Path.home() / "Downloads"
    arquivos_zip = [f for f in caminho_downloads.glob("*.zip") if f.is_file()]
    if not arquivos_zip:
        print("Nenhum arquivo .zip encontrado na pasta de downloads.")
        return
    arquivo_zip_recente = max(arquivos_zip, key=lambda f: f.stat().st_mtime)
    caminho_extracao = Path().absolute()
    with zipfile.ZipFile(arquivo_zip_recente, 'r') as zip_ref:
        zip_ref.extractall(caminho_extracao)
    print(f"Extraído: {arquivo_zip_recente.name} no diretório {caminho_extracao}")
    os.remove(arquivo_zip_recente)

listar_downloads()
extrair_ultimo_download_zip()