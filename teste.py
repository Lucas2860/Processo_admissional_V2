import json
from datetime import datetime

def ler_arquivo_json(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)
        

def alterar_data():
    ano_atual = datetime.now().year
    arquivo = ler_arquivo_json("Dados Pessoais.json")
    for i in arquivo:
        data_rg = i.get("rg_data_expedicao")
        ano = data_rg.split("/")[-1]
        if ano < ano_atual:
            ano -= 10
    print(ano)


alterar_data()