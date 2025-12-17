import os
import subprocess
import sys
from verificar_ou_clicar_imagem import emoji_status

def executar_script(script_path):
    """Executa um script Python e retorna True se for bem-sucedido"""
    try:
        print(f"{emoji_status('executando')} Iniciando execução de {script_path}")
        resultado = subprocess.run([sys.executable, script_path], check=True)
        print(f"{emoji_status('sucesso')} {script_path} executado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{emoji_status('erro')} Erro ao executar {script_path}: {e}")
        return False
    except Exception as e:
        print(f"{emoji_status('erro')} Erro inesperado ao executar {script_path}: {e}")
        return False

def main():
    # Caminhos para os codigos 
    pegar_dados_script = "pegar_dados_site.py"
    processo_sar_script = "processo_no_SAR.py"
    
    # 1. Executar pegar_dados_site.py
    sucesso_pegar_dados = executar_script(pegar_dados_script)
    
    if not sucesso_pegar_dados:
        print(f"{emoji_status('erro')} Falha na execução do pegar_dados_site.py. Abortando...")
        return
    
    
    # 3. Se pegar_dados_site.py foi bem-sucedido, executar processo_no_SAR.py
    print(f"{emoji_status('info')} Iniciando execução do processo_no_SAR.py")
    sucesso_processo_sar = executar_script(processo_sar_script)
    
    if sucesso_processo_sar:
        print(f"{emoji_status('sucesso')} Processo completo concluído com sucesso!")
    else:
        print(f"{emoji_status('erro')} Processo completo finalizado com erros")

if __name__ == "__main__":
    main()
    