
## https://www.youtube.com/watch?v=Ej7I8BPw7Gk&list=PLpeS0xTwoWAsn3SwQbSsOZ26pqZ-0CG6i   - PLAYLIST usada com base para os códigos 



import random
import argparse


from mecanica import setup_ships_randomly, verificar_tiro, is_valid_ship_placement 
from interface import setup_player_ships_handler, mostrar_tabuleiro, get_shot, get_enemy_shot
from interface import mostrar_menu_principal, mostrar_menu_pause, mostrar_menu_arquivos, mostrar_regras, mostrar_historico, mostrar_creditos , mostrar_menu_configuracoes
from arquivo import salvar_autosave, log_historico, carregar_jogo, salvar_jogo , log_erro 


CONFIG_ATUAL = {'tiros_por_turno': 5} ##### REVISAR


def parse_arguments():
   
    parser = argparse.ArgumentParser(description="Batalha Naval em Python.")
    
    parser.add_argument(
        '-n', '--novo-jogo', 
        action='store_true', 
        help='Inicia um novo jogo imediatamente, pulando o menu principal.'
    )
    
    parser.add_argument(
        '-c', '--carregar-jogo', 
        type=str, 
        metavar='NOME_ARQUIVO', 
        help='Carrega um jogo a partir do arquivo .save especificado (sem a extensão).'
    )
    
    parser.add_argument(
        '-p', '--pasta-saves', 
        type=str, 
        metavar='PASTA', 
        default='saves_batalha_naval', 
        help='Define a pasta de saves a ser utilizada (padrão: saves_batalha_naval).'
    )
    
    
    parser.add_argument(
        '-t', '--tiros-por-turno',
        type=int,
        default=5,
        help='Define o número de tiros por turno (padrão: 5).'
    )
    
    return parser.parse_args()


def iniciar_novo_jogo(args=None):
    
    
    print("🤖 Barcos Inimigos sendo posicionados aleatoriamente...")
    all_enemy_ships = setup_ships_randomly() 
    print("✅ Posicionamento do Inimigo concluído.")
    

    tiros_config_base = CONFIG_ATUAL['tiros_por_turno']
    all_player_ships = setup_player_ships_handler(is_valid_ship_placement, setup_ships_randomly)
    
    # Se args não for fornecido (chamado pelo menu), usa o padrão de 5 tiros
    tiros_por_turno = args.tiros_por_turno if args and args.tiros_por_turno else 5
    
    estado_do_jogo = {
        'enemy_ships_on_board': [s[:] for s in all_enemy_ships], 
        'player_ships_on_board': [s[:] for s in all_player_ships],
        'player_ship_coords': [coord for ship in all_player_ships for coord in ship], 
        'hit_enemy': [], 
        'miss_enemy': [],
        'afundou_enemy': [],
        'hit_player': [],
        'miss_player': [],
        'afundou_player': [],
        'rodada': 0,
        
        'config': {'tiros_por_turno': tiros_por_turno}, 
        
        'total_len_enemy': sum(len(barco) for barco in all_enemy_ships),
        'total_len_player': sum(len(barco) for barco in all_player_ships)
    }
    
    print("🔥 Todos os Barcos Posicionados. Que comece a batalha! 🔥")
    return estado_do_jogo


def pause_menu_handler(estado_do_jogo):
   
    while True:
        escolha = mostrar_menu_pause()
        
        if escolha == '4': 
            return 'VOLTAR'
        elif escolha == '3': 
            nome_arquivo = mostrar_menu_arquivos(acao="salvar")
            if nome_arquivo != 'VOLTAR':
                salvar_jogo(estado_do_jogo, nome_arquivo)
        elif escolha == '1': 
            return 'INICIAR_NOVO'
        elif escolha == '5': 
            return 'MENU_PRINCIPAL'
        elif escolha == '2': 
            nome_arquivo = mostrar_menu_arquivos(acao="carregar")
            if nome_arquivo != 'VOLTAR':
                estado_carregado = carregar_jogo(nome_arquivo)
                if estado_carregado:
                    return estado_carregado 
        elif escolha == '6': 
            print("Encerrando o programa.")
            exit()
        
        print("Voltando ao Menu de Pause...")
        

def loop_do_jogo(estado_do_jogo):
    
    rodada = estado_do_jogo['rodada']
    tiros_por_turno = estado_do_jogo['config']['tiros_por_turno']
    
    while rodada < 100:
        rodada += 1
        estado_do_jogo['rodada'] = rodada 
        
        if estado_do_jogo['total_len_enemy'] == 0 or estado_do_jogo['total_len_player'] == 0:
            break

        print(f"\n======== RODADA {rodada} ({tiros_por_turno} TIROS PARA CADA) ========")
       
        print("\n--- SEU TURNO ---")
        mostrar_tabuleiro(estado_do_jogo)

        for tiro_num in range(1, tiros_por_turno + 1):
            
            palpite_enemy = estado_do_jogo['hit_enemy'] + estado_do_jogo['miss_enemy'] + estado_do_jogo['afundou_enemy']
            tiro_jogador = get_shot(palpite_enemy) 

            print(f"[Seu Tiro {tiro_num} de {tiros_por_turno}]")
            mostrar_tabuleiro(estado_do_jogo)

            if tiro_jogador == 'PAUSE':
                acao = pause_menu_handler(estado_do_jogo)
                
                if acao in ['INICIAR_NOVO', 'MENU_PRINCIPAL'] or isinstance(acao, dict):
                    return acao 
                elif acao == 'VOLTAR':
                    continue 

            estado_do_jogo = verificar_tiro(estado_do_jogo, tiro_jogador, is_player_turn=True)

            if estado_do_jogo['total_len_enemy'] == 0:
                log_historico(estado_do_jogo, "VITÓRIA")
            
                print("\n🎉🎉 VOCÊ GANHOU! Todos os navios infiéis foram destruídos! 🎉🎉")
                break 

            print(f"Posições de barcos inimigos restantes: {estado_do_jogo['total_len_enemy']} ")

      
        if estado_do_jogo['total_len_enemy'] == 0:
            continue 

       
        print("\n--- TURNO DO INIMIGO ---")
        
        for tiro_num in range(1, tiros_por_turno + 1):
            palpite_player = estado_do_jogo['hit_player'] + estado_do_jogo['miss_player'] + estado_do_jogo['afundou_player'] 
            tiro_inimigo = get_enemy_shot(palpite_player)
            
            print(f"[Tiro inimigo {tiro_num} de {tiros_por_turno}. ]")

            estado_do_jogo = verificar_tiro(estado_do_jogo, tiro_inimigo, is_player_turn=False)

            if estado_do_jogo['total_len_player'] == 0:
                log_historico(estado_do_jogo, "DERROTA")
               
                print("\n😭😭 DERROTA TOTAL, PâNICO, CATASTROFE! O inimigo destruiu todos os seus navios. 😭😭")
                break 

            print(f"Suas posições de barcos restantes: {estado_do_jogo['total_len_player']}")

      
        if estado_do_jogo['total_len_player'] == 0:
            break 
        
        
        salvar_autosave(estado_do_jogo)
        print("[💾 Partida salva automaticamente.]")

    
    if rodada == 100 and estado_do_jogo['total_len_enemy'] > 0 and estado_do_jogo['total_len_player'] > 0:
        log_historico(estado_do_jogo, "EMPATE/LIMITE")
        print("FIM DE JOGO: Você atingiu o limite de 100 rodadas. Jogo empatado. ⚠️ ")

    print("\n--- ESTATÍSTICAS FINAIS ---")
    mostrar_tabuleiro(estado_do_jogo)

    return 'MENU_PRINCIPAL'



def main_menu_handler():
    
    while True:
        escolha = mostrar_menu_principal()

        if escolha == '1':
            novo_estado = iniciar_novo_jogo()
            retorno_loop = loop_do_jogo(novo_estado)
            
           
            if retorno_loop == 'MENU_PRINCIPAL':
                continue 
            elif retorno_loop == 'SAIR':
                return 'SAIR' 
            elif isinstance(retorno_loop, dict):
                 retorno_loop = loop_do_jogo(retorno_loop)
                 if retorno_loop == 'MENU_PRINCIPAL':
                    continue
            
        elif escolha == '2':
            nome_arquivo = mostrar_menu_arquivos(acao="carregar")
            if nome_arquivo != 'VOLTAR':
                estado_carregado = carregar_jogo(nome_arquivo)
                if estado_carregado:
                    retorno_loop = loop_do_jogo(estado_carregado)
                    
                    if retorno_loop == 'MENU_PRINCIPAL':
                         continue
                    elif retorno_loop == 'SAIR':
                         return 'SAIR'
                else:
                    continue 
            
        elif escolha == '3': 
            mostrar_regras()
            continue 
            
        elif escolha == '4': 
            mostrar_historico()
            continue 
            
        elif escolha == '5':
            mostrar_creditos()
            continue 
            
        elif escolha == '6':
            estado_config_temp = {'config': CONFIG_ATUAL}
            mostrar_menu_configuracoes(estado_config_temp)

            continue
        elif escolha == '7':
            print("Encerrando o joguinho Batalha Naval. Até mais! :)")
            return 'SAIR'

def main():
    
    
    args = parse_arguments()
    
    
    global CONFIG_ATUAL ########## REVISAR ESSE GLOBAL
    if args.tiros_por_turno != 5: 
        CONFIG_ATUAL['tiros_por_turno'] = args.tiros_por_turno
        
        if args.novo_jogo:
            print("Iniciando novo jogo via argumento de console...")
            estado_do_jogo = iniciar_novo_jogo(args) 
            
        elif args.carregar_jogo:
            print(f"Tentando carregar jogo: {args.carregar_jogo}")
            estado_do_jogo = carregar_jogo(args.carregar_jogo)
            
            if not estado_do_jogo:
                print("Não foi possível carregar o jogo. Abrindo Menu Principal.")
                log_erro (f"Falha ao carregar jogo '{args.carregar_jogo}' via Argumento de Console.") 
                return main_menu_handler()
        
      
        if estado_do_jogo:
            loop_do_jogo(estado_do_jogo)
            
    else:
      
        main_menu_handler()
        
if __name__ == "__main__":
    main()