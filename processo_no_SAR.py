import subprocess
import time
import psutil
import os
import pyautogui as pag
import json
from unidecode import unidecode
import keyboard
import clipboard
from datetime import datetime
import re

#lista com os codigos dos paises usados no cadastro
codigospaises = {13: 'AFEGANISTAO',15: 'ALAND, ILHAS', 17: 'ALBANIA, REPUBLICA DA', 23: 'ALEMANHA', 31: 'BURKINA FASO', 37: 'ANDORRA', 40: 'ANGOLA', 41: 'ANGUILLA', 42: 'ANTÁRTICA', 43: 'ANTIGUA E BARBUDA', 53: 'ARABIA SAUDITA', 59: 'ARGELIA', 63: 'ARGENTINA', 64: 'ARMENIA, REPUBLICA DA', 65: 'ARUBA', 69: 'AUSTRALIA', 72: 'AUSTRIA', 73: 'AZERBAIJAO, REPUBLICA DO', 77: 'BAHAMAS, ILHAS', 80: 'BAHREIN, ILHAS', 81: 'BANGLADESH', 83: 'BARBADOS', 85: 'BELARUS, REPUBLICA DA', 87: 'BELGICA', 88: 'BELIZE', 90: 'BERMUDAS', 93: 'MIANMAR (BIRMANIA)', 97: 'BOLIVIA, ESTADO PLURINACIONAL DA', 98: 'BOSNIA-HERZEGOVINA (REPUBLICA DA)', 99: 'BONAIRE, SAINT EUSTATIUS E SABA', 101: 'BOTSUANA', 102: 'BOUVET, ILHA', 105: 'BRASIL', 108: 'BRUNEI', 111: 'BULGARIA, REPUBLICA DA', 115: 'BURUNDI', 119: 'BUTAO', 127: 'CABO VERDE, REPUBLICA DE', 137: 'CAYMAN, ILHAS', 141: 'CAMBOJA', 145: 'CAMAROES', 149: 'CANADA', 153: 'CAZAQUISTAO, REPUBLICA DO', 154: 'CATAR', 158: 'CHILE', 160: 'CHINA, REPUBLICA POPULAR', 161: 'FORMOSA (TAIWAN)', 163: 'CHIPRE', 165: 'COCOS(KEELING),ILHAS', 169: 'COLOMBIA', 173: 'COMORES, ILHAS', 177: 'CONGO', 183: 'COOK, ILHAS', 187: 'COREIA (DO NORTE), REP.POP.DEMOCRATICA', 190: 'CORÉIA, REPÚBLICA DA', 193: 'COSTA DO MARFIM', 195: 'CROACIA (REPUBLICA DA)', 196: 'COSTA RICA', 198: 'COVEITE', 199: 'CUBA', 200: 'CURACAO', 229: 'BENIN', 232: 'DINAMARCA', 235: 'DOMINICA, ILHA', 239: 'ECUADOR', 240: 'EGITO', 243: 'ERITREIA', 244: 'EMIRADOS ÁRABES UNIDOS', 245: 'ESPANHA', 246: 'ESLOVÊNIA, REPÚBLICA DA', 247: 'ESLOVACA, REPÚBLICA DA', 249: 'ESTADOS UNIDOS', 251: 'ESTÔNIA, REPÚBLICA DA', 253: 'ETIÓPIA', 255: 'FALKLAND (ILHAS MALVINAS)', 259: 'FEROE, ILHAS', 267: 'FILIPINAS', 271: 'FINLÂNDIA', 275: 'FRANÇA', 281: 'GABÃO', 285: 'GAMBIA', 289: 'GANA', 291: 'GEORGIA, REPÚBLICA DA', 292: 'GEÓRGIA DO SUL E SANDWICH DO SUL, ILHAS', 293: 'GIBRALTAR', 297: 'GRANADA', 301: 'GRÉCIA', 305: 'GROELÃNDIA', 309: 'GUADALUPE', 313: 'GUAM', 317: 'GUATEMALA', 321: 'GUERNSEY', 325: 'GUIANA FRANCESA', 329: 'GUINÉ', 334: 'GUINE-BISSAU', 331: 'GUINÉ-EQUATORIAL', 337: 'GUIANA', 341: 'HAITI', 343: 'HEARD E ILHAS MCDONALD, ILHA', 345: 'HONDURAS', 351: 'HONG KONG', 355: 'HUNGRIA, REPUBLICA DA', 357: 'IEMEN', 359: 'MAN, ILHA DE', 361: 'ÍNDIA', 365: 'INDONÉSIA', 369: 'IRAQUE', 372: 'IRÃ, REPUBLICA ISLÂMICA DO', 375: 'IRLANDA', 379: 'ISLÂNDIA', 383: 'ISRAEL', 386: 'ITÁLIA', 391: 'JAMAICA', 393: 'JERSEY', 399: 'JAPÃO', 403: 'JORDÂNIA', 411: 'KIRIBATI', 420: 'LAOS, REP.POP.DEMOCR.DO', 426: 'LESOTO', 427: 'LETÔNIA, REPÚBLICA DA', 431: 'LÍBANO', 434: 'LIBÉRIA', 438: 'LÍBIA', 440: 'LIECHTENSTEIN', 442: 'LITUÂNIA, REPÚBLICA DA', 445: 'LUXEMBURGO', 447: 'MACAU', 449: 'MACEDÔNIA, ANT.REP.IUGOSLAVA', 450: 'MADAGASCAR', 455: 'MALÁSIA', 458: 'MALAVI', 461: 'MALDIVAS', 464: 'MALI', 467: 'MALTA', 472: 'MARIANAS DO NORTE', 474: 'MARROCOS', 476: 'MARSHALL, ILHAS', 477: 'MARTINICA', 485: 'MAURÍCIO', 488: 'MAURITÂNIA', 489: 'MAYOTTE', 493: 'MEXICO', 494: 'MOLDAVIA, REPÚBLICA DA', 495: 'MÔNACO', 497: 'MONGÓLIA', 498: 'MONTENEGRO', 499: 'MICRONÉSIA', 501: 'MONTSERRAT, ILHAS', 505: 'MOÇAMBIQUE', 507: 'NAMÍBIA', 508: 'NAURU', 511: 'CHRISTMAS,ILHA (NAVIDAD)', 517: 'NEPAL', 521: 'NICARÁGUA', 525: 'NIGER', 528: 'NIGÉRIA', 531: 'NIUE, ILHA', 535: 'NORFOLK, ILHA', 538: 'NORUEGA', 542: 'NOVA CALEDÔNIA', 545: 'PAPUA NOVA GUINÉ', 548: 'NOVA ZELÂNDIA', 551: 'VANUATU', 556: 'OMÃ', 566: 'PACIFICO, ILHAS DO (POSSESSAO DOS EUA)', 573: 'PAÍSES BAIXOS (HOLANDA)', 575: 'PALAU', 576: 'PAQUISTÃO', 578: 'PALESTINA', 580: 'PANAMÁ', 586: 'PARAGUAI', 589: 'PERU', 593: 'PITCAIRN, ILHA DE', 599: 'POLINÉSIA FRANCESA', 603: 'POLÔNIA, REPÚBLICA DA', 607: 'PORTUGAL', 611: 'PORTO RICO', 623: 'QUÊNIA', 625: 'QUIRGUIZ, REPÚBLICA DA', 628: 'REINO UNIDO', 640: 'REPÚBLICA CENTRO-AFRICANA', 647: 'REPÚBLICA DOMINICANA', 660: 'REUNIÃO, ILHA', 665: 'ZIMBABUE', 670: 'ROMÊNIA', 675: 'RUANDA', 676: 'RUSSIA, FEDERAÇÃO DA', 677: 'SALOMÃO, ILHAS', 685: 'SAARA OCIDENTAL', 687: 'EL SALVADOR', 690: 'SAMOA', 691: 'SAMOA AMERICANA', 693: 'SAO BARTOLOMEU', 695: 'SÃO CRISTOVÃO E NEVES, ILHAS', 697: 'SAN MARINO', 698: 'SÃO MARTINHO, ILHA DE (PARTE FRANCESA)', 699: 'SÃO MARTINHO, ILHA DE (PARTE HOLANDESA)', 700: 'SÃO PEDRO E MIQUELON', 705: 'SÃO VICENTE E GRANADINAS', 710: 'SANTA HELENA', 715: 'SANTA LÚCIA', 720: 'SÃO TOMÉ E PRÍNCIPE, ILHAS', 728: 'SENEGAL', 731: 'SEYCHELLES', 735: 'SERRA LEOA', 737: 'SERVIA', 741: 'CINGAPURA', 744: 'SÍRIA, REPÚBLICA ARABE DA', 748: 'SOMÁLIA', 750: 'SRI LANKA', 754: 'SUAZILÂNDIA', 755: 'SVALBARD E JAN MAYEN', 756: 'AFRICA DO SUL', 759: 'SUDÃO', 760: 'SUDAO DO SUL', 764: 'SUÉCIA', 767: 'SUÍCA', 770: 'SURINAME', 772: 'TADJIQUISTÃO, REPÚBLICA DO', 776: 'TAILÂNDIA', 780: 'TANZANIA, REP. UNIDA DA', 781: 'TERRAS AUSTRAIS FRANCESAS', 782: 'TERRITÓRIO BRITÂNICO NO OCEANO ÍNDICO', 783: 'DJIBUTI', 788: 'CHADE', 791: 'TCHECA, REPUBLICA', 795: 'TIMOR LESTE', 800: 'TOGO', 805: 'TOQUELAU, ILHAS', 810: 'TONGA', 815: 'TRINIDAD E TOBAGO', 820: 'TUNÍSIA', 823: 'TURCAS E CAICOS, ILHAS', 824: 'TURCOMENISTÃO, REPUBLICA DO', 827: 'TURQUIA', 828: 'TUVALU', 831: 'UCRÂNIA', 833: 'UGANDA', 845: 'URUGUAI', 847: 'UZBEQUISTÃO, REPÚBLICA DO', 848: 'VATICANO, EST. DA CIDADE DO', 850: 'VENEZUELA', 858: 'VIETNÃ', 863: 'VIRGENS, ILHAS (BRITÂNICAS)', 866: 'VIRGENS, ILHAS (E.U.A.)', 870: 'FIJI', 875: 'WALLIS E FUTUNA, ILHAS', 888: 'CONGO, REPUBLICA DEMOCRATICA DO', 890: 'ZÂMBIA'}

# Variável para o caminho do programa/atalho
programa_abrir = r"C:\Program Files (x86)\HK\SAR2G\SarClient\SarClient.exe"

listadocs = ["cpf","nome","celular","email","data_nascimento","pais_nascimento","nacionalidade","sexo","estado_civil","raca","cidade_nascimento","uf_nascimento","Grau_instrucao"]
exe_processo = "SarClient.exe"
txtpess = r"R:\RPA\Publico\Livre\ProcessoAdmissional.txt"
txtpess1 = r"R:\RPA\Publico\Livre\ProcessoAdmissionalNF.txt"

from verificar_ou_clicar_imagem import apenasverificar,clickimagem,emoji_status,doubleclickimagem

#ENTRANDO NO SAR
def verificar_processo(processo):
    """
    Verifica se o processo está em execução
    
    Args:
        processo (str): Nome do executável a ser verificado
    
    Returns:
        bool: True se o processo está rodando, False caso contrário
    """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == processo:
            return True
    return False

def matar_processo(processo):
    """
    Mata o processo especificado
    
    Args:
        processo (str): Nome do executável a ser finalizado
    
    Returns:
        bool: True se o processo foi finalizado com sucesso, False caso contrário
    """
    try:
        # Usa o comando taskkill para finalizar o processo
        subprocess.run(f'taskkill /F /IM {processo}', 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            shell=True, 
            text=True)
        print(f"{emoji_status('finalizado')} Processo {processo} finalizado com sucesso!")
        return True
    except Exception as e:
        print(f"{emoji_status('erro')} Erro ao finalizar o processo {processo}: {e}")
        return False

def abrir_programa():
    """
    Abre o programa especificado
    
    Returns:
        bool: True se o programa foi aberto com sucesso, False caso contrário
    """
    try:
        # Verifica se o arquivo existe
        if os.path.exists(programa_abrir):
            # Usa o comando start para abrir o atalho ou executável
            subprocess.Popen(f'start "" "{programa_abrir}"', shell=True)
            print(f"{emoji_status('sucesso')} Programa {programa_abrir} aberto com sucesso!")
            return True
        else:
            print(f"{emoji_status('erro')} Erro: Arquivo não encontrado em {programa_abrir}")
            return False
    except Exception as e:
        print(f"{emoji_status('erro')} Erro ao abrir o programa: {e}")
        return False

def autenticar_sistema():
    """
    Realiza o login no sistema
    
    Returns:
        bool: True se a autenticação for bem-sucedida, False caso contrário
    """
    try:

        # Espera a tela de autenticação usando a nova função
        if not apenasverificar('login_SAR.png'):
            return False

        print(f"{emoji_status('info')} Realizando login no sistema")

        # Digita login
        pag.write("rpa.aster")
        time.sleep(0.2)
        pag.press('tab')
        time.sleep(0.2)
        
        # Digita senha
        pag.write("Atsoc!GfD4C31")
        time.sleep(0.2)
        pag.press('enter')
        
        # Adiciona um tempo para processar a autenticação e o processo abrir.
        time.sleep(5)

        # Espera pela tela inicial do service
        if not apenasverificar('tela_inicial_SAR.png'):
            return False

        print(f"{emoji_status('sucesso')} Login realizado com sucesso!")
        
        # Chama a função de execução de rotinas
        return executar_rotinas_sistema()

    except Exception as e:
        print(f"{emoji_status('erro')} Erro durante a autenticação: {e}")
        return False

def calcular_idade(data_nascimento):
    try:
        if "/" in data_nascimento:
            nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        elif "-" in data_nascimento:
            nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
        else:
            raise ValueError
        hoje = datetime.now()
        idade = hoje.year - nascimento.year
        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1
        return idade
    except ValueError:
        return -1  # Valor padrão para erros

def extrair_orgao_emissor(dados):
    # Tenta ambos os possíveis nomes de chave
    bruto = (dados.get("rg_orgao_emissor")
             or dados.get("rg_estado_emissor")
             or "")
    # Se não for string, evita erro
    bruto = str(bruto)
    # Divide no primeiro hífen (pega -, – ou —) e remove espaços
    orgao = re.split(r"\s*[-–—]\s*", bruto, maxsplit=1)[0].strip()
    return orgao

def verificar_deficiencias(dados):
    deficiencias_map = {
        "deficiencia_auditiva": "Auditiva",
        "deficiencia_fisica": "Física",
        "deficiencia_mental": "Mental",
        "deficiencia_visual": "Visual",
        "deficiencia_intelectual": "Intelectual",
        "deficiencia_reabilitacao": "Reabilitação"
    }
    
    deficiencias_encontradas = [
        deficiencias_map[chave] for chave, valor in dados.items() if chave in deficiencias_map and valor == "1"
    ]
    if not deficiencias_encontradas:
        return "Nenhuma deficiência encontrada."
    if len(deficiencias_encontradas) == 1:
        return deficiencias_encontradas[0]
    return deficiencias_encontradas

def executar_rotinas_sistema():
    """
    Executa as rotinas automatizadas após login
    
    Returns:
        bool: True se todas as rotinas foram executadas com sucesso, False caso contrário
    """
    time.sleep(2) # TEMPO PARA O SERVICE CARREGAR OS MENUS
    try:
        # Espera a tela inicial do service
        if not apenasverificar('tela_inicial_SAR.png'):
            print(f"{emoji_status('erro')} Tela inicial do service não encontrada")
            return False
        
        print(f"{emoji_status('sucesso')} Rotinas executadas com sucesso!")
        return True
    
    except Exception as e:
        print(f"{emoji_status('erro')} Erro durante execução de rotinas: {e}")
        return False

def gerenciar_processo(processo):
    """
    Gerencia o processo: verifica, mata se necessário, reabre e autentica
    
    Args:
        processo (str): Nome do executável
    
    Returns:
        bool: Status final da operação
    """
    # Verifica se o processo está rodando
    if verificar_processo(processo):
        print(f"{emoji_status('executando')} Processo {processo} está em execução.")
        
        # Tenta matar o processo
        if matar_processo(processo):
            # Adiciona um pequeno delay para garantir que o processo seja encerrado
            time.sleep(2)
    
    # Verifica novamente se o processo foi encerrado
    if not verificar_processo(processo):
        # Tenta abrir o programa
        if abrir_programa():
            # Tenta autenticar
            return autenticar_sistema()
    
    print(f"{emoji_status('erro')} Não foi possível processar {processo}")
    return False

def ler_arquivo_json(caminho_arquivo):
    global dados
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return dados

def checarinfor(dados):
    for dado in listadocs:
        if dados[dado] == "":
            return True
    return False

#ALTERANDO AS DATAS DE EXPEDIÇÃO DO RG
def alterar_data():
    arquivo = ler_arquivo_json("Dados Pessoais.json")
    data_rg = arquivo["rg_data_expedicao"]
    print(data_rg)

def checkexistente(cpf):
    # Verifica se o CPF está vazio
    if not cpf or cpf.strip() == "":
        print(f"{emoji_status('info')} CPF vazio, pulando para o próximo candidato.")
        return None  # Retorna None para indicar que o CPF está vazio
    apenasverificar('lupa_aba_candidatos.png')
    clickimagem('lupa_aba_candidatos.png')
    time.sleep(2)
    apenasverificar('area_pesquisa_candidatos.png')
    pag.press('tab')
    pag.press("space")
    pag.press('tab',presses=5)
    keyboard.write(cpf)
    clickimagem('pesquisar_candidato.png')
    cadastrado = apenasverificar("1_achados.png",timeout=3,threshold=0.9)
    if cadastrado == True:
        clickimagem('fechar_nao_achado.png')
        return
    elif apenasverificar("2_achados.png",timeout=3,threshold=0.9):
        clickimagem('fechar_nao_achado.png')
        return
    clickimagem('ok_sem_retorno.png')
    pag.press("tab")
    pag.press("space")
    clickimagem('pesquisar_candidato.png')
    cadastrado = apenasverificar("1_achados.png",timeout=3,threshold=0.9)
    if cadastrado == True:
        clickimagem('fechar_nao_achado.png')
        return
    elif apenasverificar("2_achados.png",timeout=3,threshold=0.9):
        clickimagem('fechar_nao_achado.png')
        return
    apto = apenasverificar('nao_achado.png')
    clickimagem('ok_sem_retorno.png')
    clickimagem('fechar_nao_achado.png')
    return apto
    
def cadastrodepend(dados):
    for i in range(len(dados)):
        if dados[i]["cpf_dependente"] == "":
            continue
        
        clickimagem('novo_dependente.png')

        apenasverificar('adicionar.png')
        clickimagem('adicionar.png')
        
        time.sleep(0.5)
        clipboard.copy(dados[i]["nome_dependente"])
        pag.hotkey("ctrl","v")
        
        pag.press("tab")
        time.sleep(0.2)
        keyboard.write(dados[i]["parentesco_label"])
        if dados[i]["parentesco_label"] == "Filho(a) ou enteado(a)":
            keyboard.write("FILHO")
        else:
            pag.hotkey("ctrl","v")
        pag.press("tab", presses=1)
        keyboard.write("NÃO")

        rotulo = dados[i].get("parentesco_label", "")

        if rotulo in (
            "Filho(a) ou enteado(a)",
            "Filho(a) ou enteado(a), universitário(a) ou cursando escola técnica de 2º grau",
        ):
            pag.press("tab", presses=3)
            keyboard.write("NÃO")

        clickimagem('tipo_esocial.png')
        keyboard.write(dados[i]["parentesco_label"])

        apenasverificar('aba_dados_cadastrais.png')
        clickimagem('aba_dados_cadastrais.png')

        '''if dados[i]["parentesco_label"] == "Filho(a) ou enteado(a)":
            pag.press("tab", presses=3)
            keyboard.write("NÃO")
            clickimagem('data_obito.png')
            time.sleep(0.1)
            pag.press("tab", presses=2)
        elif dados[i]["parentesco_label"] == "Cônjuge":
            pag.press("tab", presses=4)
        else:
            pag.press("tab", presses=7)'''
        
        time.sleep(0.4)
        pag.press("tab")
        time.sleep(0.4)

        if dados[i]["sexo"] == "2":
            pag.write("FEMININO")
        else:
            pag.write("MASCULINO")
        
        time.sleep(0.4)
        pag.press("tab", presses=4)

        clipboard.copy(dados[i]["data_nascimento"])
        pag.hotkey("ctrl","v")

        time.sleep(0.4)
        pag.press("tab", presses=3)

        clipboard.copy(dados[i]["cpf_dependente"])
        pag.hotkey("ctrl","v")

        apenasverificar('salvar1.png')
        clickimagem('salvar1.png')
        apenasverificar('fechar.png')
        clickimagem('fechar.png')

def cadastrandonovo(dados):
    time.sleep(2)
    clickimagem('novo_area_candidato.png')
    apenasverificar('adicionar.png')
    clickimagem('adicionar.png')
    time.sleep(1)
    clipboard.copy(unidecode(dados["nome"]))
    time.sleep(0.5)
    pag.hotkey("ctrl","v")
    pag.press("tab", presses=3)
    if dados["sexo"] == "2":
        pag.write("FEMININO")
    else:
        pag.write("MASCULINO")
    pag.press("tab",presses=3)
    time.sleep(1)
    cod = codigospaises[int(dados["pais_nascimento"])]
    clipboard.copy(cod)
    print(cod)
    time.sleep(0.5)
    pag.write(cod)
    pag.press("tab")
    datanasciori = dados["data_nascimento"]
    datanasci = int(dados["data_nascimento"][6:])
    clipboard.copy(dados["data_nascimento"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")
    pag.press("tab")
    clipboard.copy(dados["uf_nascimento"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")  
    time.sleep(0.5)
    pag.press("tab")
    clipboard.copy(dados["cidade_nascimento"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v") 
    pag.press("tab")
    clipboard.copy(dados["cpf"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")  
    pag.press("tab")
    #POSSIVEL AVISO
    cadastrado = apenasverificar("erro_cpf_ja_cadastrado.png",timeout=3)
    if cadastrado == True:
        clickimagem("ok_sem_retorno.png")
        clickimagem("voltar.png")
        return
    #--------
    #LOGICA ORGÂO EMISSOR

    def cadastro_rg():
        bruto = str(dados.get("rg_orgao_emissor", "")).strip()

        # Extrai Órgão e UF a partir de "SSP - SP" (aceita -, – ou —)
        if bruto.upper() == "Outro":
            orgao = "SSP"
            uf = "SP"  # default seguro
        else:
            orgao = dados.get("rg_orgao_emissor")
            uf = dados.get("rg_estado_emissor")

        # Preenche: Número RG -> Órgão -> UF -> Data de expedição
        clipboard.copy(dados.get("rg_numero", ""))
        time.sleep(0.5)
        pag.hotkey("ctrl", "v")

        pag.press("tab")
        pag.write(orgao, interval=0.2)

        pag.press("tab")
        pag.write(uf)

        pag.press("tab")
        clipboard.copy(dados.get("rg_data_expedicao", ""))
        time.sleep(0.5)
        pag.hotkey("ctrl", "v")

    if dados["rg_orgao_emissor"] == "":
        print("SEM RG")
        pag.press("tab", presses=5)
    else:
        cadastro_rg()
        pag.press("tab", presses=2)

    clipboard.copy(dados["reservista_ra"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")
    pag.press("tab", presses=4)
    clipboard.copy(dados["ctps_pispasep"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")
    pag.press("tab", presses=1)
    if dados["ctps_pispasep"]:
        if datanasci < 1999:
            clipboard.copy("01/01/2000")
        elif datanasci < 2009: 
            time.sleep(0.5)
            clipboard.copy("01/01/2010")
        pag.hotkey("ctrl","v")
        
    pag.press("tab", presses=12)
    clipboard.copy(dados["titulo_eleitor_num_inscricao"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")

    pag.press("tab", presses=1)
    clipboard.copy(dados["titulo_eleitor_data_emissao"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")

    pag.press("tab", presses=1)
    clipboard.copy(dados["titulo_eleitor_zona"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")

    pag.press("tab", presses=1)
    clipboard.copy(dados["titulo_eleitor_secao"])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")

    pag.press("tab", presses=1)
    clipboard.copy(dados["titulo_eleitor_cidade"][-2:])
    time.sleep(0.5)
    pag.hotkey("ctrl","v")
    apenasverificar('aba_dadosRH.png')
    clickimagem('aba_dadosRH.png')
    if apenasverificar("aba_sados_rh.png") == False:
        clickimagem('aba_dadosRH.png')
    
    pag.press("tab", presses=1)
    pag.write("NÃO")
    pag.press("tab", presses=2)
    pag.write("NÃO")
    pag.press("tab", presses=2)
    pag.write("NÃO")
    pag.press("tab", presses=1)
    if calcular_idade(datanasciori) > 18:
        pag.write("NÃO")
    else:
        pag.write("SIM")
    pag.press("tab", presses=2)
    estadocivil = dados["estado_civil"]
    match estadocivil:
        case "1":
            pag.write("SOLTEIRO")
        case "2":
            pag.write("CASADO")
        case "uniao":
            pag.write("UNIÃO ESTAvEL")
        case "4":
            pag.write("DIvORcIADO")
    
    pag.press("tab", presses=1)
    escolaridade = dados["Grau_instrucao"]
    if escolaridade == "Técnico/Pós-Médio Completo":
        pag.write("2")
        pag.press("enter")
    else:
        pag.write(escolaridade)

    pag.press("tab", presses=1)

    deficienciasgerais = {
        "Auditivo": dados["deficiencia_auditiva"],
        "Físico": dados["deficiencia_fisica"],
        "Mental": dados["deficiencia_mental"],
        "Visual": dados["deficiencia_visual"],
        "Intelectual": dados["deficiencia_intelectual"],
        "Reabilitado": dados["deficiencia_reabilitacao"]
    }

    mensagem = verificar_deficiencias(dados)
    print(type(mensagem))
    if mensagem == "Nenhuma deficiência encontrada.":
        pag.write("NÃO")
    elif len(mensagem) > 1:
        keyboard.write("MÚLTIPLAS")
    else:
        pag.write(mensagem)

    pag.press("tab", presses=1)
    pag.write("NÃO")
    pag.press("tab", presses=10)
    cor = dados["raca"]
    match cor:
        case "2":
            pag.write("Branca")
        case "8":
            pag.write("Parda")
        case "4":
            pag.write("Negra")
    
    cargo = dados["categoria"]
    if cargo == "VIGILANTE":
        #Logica...
        pass

    apenasverificar("salvar1.png")
    clickimagem("salvar1.png")
    for tab in range(3):  
        pag.press('tab')
    for seta in range(5):
        pag.press('right')

    if dados["nome_mae"] == "":
        pass
    else:
        apenasverificar("novo_dependente.png")
        clickimagem("novo_dependente.png")
        time.sleep(2)
        apenasverificar("adicionar.png")
        clickimagem("adicionar.png")

        clipboard.copy(dados["nome_mae"])
        time.sleep(0.2)
        pag.hotkey("ctrl","v")
        pag.press("tab", presses=1)
        keyboard.write("MÃE")
        pag.press("tab", presses=1)
        keyboard.write("NÃO")

        clickimagem("salvar1.png")

        clickimagem("fechar.png")
    if dados["nome_pai"] == "":
        pass
    else:
        apenasverificar("novo_dependente.png")
        clickimagem("novo_dependente.png")
        time.sleep(2)
        apenasverificar("adicionar.png")
        clickimagem("adicionar.png")

        time.sleep(1)

        clipboard.copy(dados["nome_pai"])
        pag.hotkey("ctrl","v")
        pag.press("tab", presses=1)
        keyboard.write("PAI")
        pag.press("tab", presses=1)
        keyboard.write("NÃO")

        clickimagem("salvar1.png")

        clickimagem("fechar.png")

    dadosdependentes = ler_arquivo_json("Dependentes.json")
    pessoas_encontradas = [p for p in dadosdependentes if p["nome_resp"] == dados["nome"]]
    if pessoas_encontradas:
        cadastrodepend(pessoas_encontradas)


#PROCESSO NO SAR

#Processando os candidatos
def process_principal():
    #Indo para a área do candidato
    pag.press('alt')
    time.sleep(2)
    pag.press('m')  
    time.sleep(2)
    pag.press('e')
    apenasverificar('candidatos.png')
    doubleclickimagem('candidatos.png')
    dadospessoais = ler_arquivo_json("Dados Pessoais.json")
    print(len(dadospessoais))
    for i in range(len(dadospessoais)):
        # Verifica se o CPF está vazio antes de chamar checkexistente
        if not dadospessoais[i]["nome"] or dadospessoais[i]["nome"].strip() == "":
            print(f"{emoji_status('info')} CPF vazio para {dadospessoais[i]['nome']}, pulando para o próximo.")
            continue
        
        apto = checkexistente(unidecode(dadospessoais[i]["nome"]))
        if apto == True:
            if checarinfor(dadospessoais[i]) == False:
                cadastrandonovo(dadospessoais[i])
            else:
                with open(txtpess1, 'a') as pessoas:
                    pessoas.write(dadospessoais[i]["nome"] + "\n")

# Bloco Principal
if __name__ == "__main__":
    # Executa o processo de gerenciamento
    resultado_gerenciamento = gerenciar_processo(exe_processo)
    
    if resultado_gerenciamento:
        # Executa rotinas do sistema
        resultado_sistema = executar_rotinas_sistema()
        process_principal()
    else:
        print(f"{emoji_status('erro')} Falha ao executar rotinas do sistema")

    #matar_processo(exe_processo)