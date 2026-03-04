import os
from datetime import datetime


SAVE_FOLDER = "saves_batalha_naval"
HISTORY_FILE = os.path.join(SAVE_FOLDER, "historico_partidas.txt")
AUTOSAVE_FILENAME = "autosave" 


def _garantir_pasta_saves():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)


def salvar_jogo(estado_do_jogo, nome_arquivo):
    
    _garantir_pasta_saves()
    
    caminho_completo = os.path.join(SAVE_FOLDER, f"{nome_arquivo}.save")
    
    try:
        with open(caminho_completo, 'w') as f:
           
            for chave, valor in estado_do_jogo.items():
                f.write(f"{chave}:{repr(valor)}\n")
        
        print(f"Jogo salvo com sucesso em: {caminho_completo}")
        return True
    except Exception as e:
        log_erro(f"Erro ao salvar jogo '{nome_arquivo}': {e}")
        print(f"Erro ao salvar o jogo: {e}")
        return False


def carregar_jogo(nome_arquivo):
   
    _garantir_pasta_saves()
    caminho_completo = os.path.join(SAVE_FOLDER, f"{nome_arquivo}.save")
    
    if not os.path.exists(caminho_completo):
        print(f"Arquivo de save '{nome_arquivo}.save' não encontrado.")
        return None
    
    estado_carregado = {}
    
    try:
        with open(caminho_completo, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                
                chave, valor_str = linha.split(":", 1)
                
             
                estado_carregado[chave] = eval(valor_str)
                
        print(f"Jogo carregado com sucesso de: {caminho_completo}")
        return estado_carregado
    except Exception as e:
        log_erro(f"Erro ao carregar jogo (eval/estrutura): {e}")
        print(f"Erro ao carregar o jogo. Arquivo corrompido: {e}")
        return None


def salvar_autosave(estado_do_jogo):
  
    return salvar_jogo(estado_do_jogo, AUTOSAVE_FILENAME)


def log_historico(estado_final, resultado):
 
    _garantir_pasta_saves()
    
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rodadas = estado_final.get('rodada', 'N/A')
    
    linha_log = (
        f"[{data_hora}] | Resultado: {resultado} | Rodadas: {rodadas} | "
        f"Inimigo Restante: {estado_final['total_len_enemy']} | "
        f"Jogador Restante: {estado_final['total_len_player']}\n"
    )
    
    try:
        with open(HISTORY_FILE, 'a') as f:
            f.write(linha_log)
        return True
    except Exception as e:
        log_erro(f"Erro ao escrever no histórico: {e}")
        return False


def log_erro(mensagem):

    _garantir_pasta_saves()
    LOG_FILE = os.path.join(SAVE_FOLDER, "log_erros.txt")
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{data_hora}] ERRO: {mensagem}\n")
    except:
        pass