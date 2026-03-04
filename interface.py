import random
import os

from arquivo import SAVE_FOLDER, HISTORY_FILE, log_erro, carregar_jogo, salvar_jogo


def mostrar_menu_configuracoes(estado_do_jogo):
    
    

    config = estado_do_jogo['config']
    
    while True:
        print("\n" + "=" * 40)
        print("    🕹️    MENU DE CONFIGURAÇÕES   🕹️     ")
        print("=" * 40)
        print(f"1. Tiros por Turno: {config['tiros_por_turno']}")
        print("V. Voltar")
        print("-" * 40)
        
        escolha = input("Escolha a opção para alterar (1 ou V): ").strip().upper()
        
        if escolha == 'V':
            return estado_do_jogo
        elif escolha == '1':
            try:
                novo_valor = int(input("Novo valor para Tiros por Turno (1-10): "))
                if 1 <= novo_valor <= 10:
                    config['tiros_por_turno'] = novo_valor
                    print(f"Configuração salva: Tiros por Turno = {novo_valor}")
                    # Retorna para reexibir o menu atualizado
                    continue 
                else:
                    print("Valor inválido. Insira um número entre 1 e 10.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número inteiro.")
        else:
            print("Opção inválida.")


def get_ship_position(board_ships, ship_size, is_valid_placement_func):
   
    while True:
        try:
            print(f"--- Posicionando barco de tamanho {ship_size} --- 🫵" )
            start = int(input(f"Escolha a posição inicial (0-99) para o barco de tamanho {ship_size}: "))
            
            direction = input("Escolha a direção (h para horizontal, v para vertical): ").strip().lower()

            if not (0 <= start <= 99):
                print("Posição inicial inválida (fora do 0-99).")
                continue
                
            if direction not in ['h', 'v']:
                print("Direção inválida. Escolha 'h' ou 'v'.")
                continue
            
            is_valid, ship_coords = is_valid_placement_func(board_ships, start, ship_size, direction)

            if is_valid:
                return ship_coords
            else:
                print("Colocação inválida! O barco sai do tabuleiro ou colide com outro. Tente novamente.")

        except ValueError:
            print("Entrada inválida. Por favor, insira um número para a posição.")
            log_erro("Valor não numérico inserido para posição inicial do barco.")


def escolher_posicionamento_jogador():
    
    print("\n--- POSICIONAMENTO DOS SEUS BARCOS  ---")
    print("1. 🃏 Posicionamento Manual (Escolher as coordenadas) ")
    print("2. Posicionamento Aleatório (Automático)")
    
    while True:
        escolha = input("Escolha o método de posicionamento (1 ou 2): ").strip()
        if escolha == '1':
            return 'manual'
        elif escolha == '2':
            return 'aleatorio'
        print("Opção inválida. Escolha 1 ou 2.")
        

def setup_player_ships_handler(is_valid_placement_func, setup_random_func):
   
    
    metodo = escolher_posicionamento_jogador()
    
    if metodo == 'aleatorio':
        print("🚢 Posicionamento Aleatório selecionado. Seus barcos estão sendo colocados...")
        all_ships = setup_random_func()
        print("✅ Seu posicionamento aleatório concluído.")
        return all_ships
    else: # Manual
        ship_sizes = [4, 3, 2] 
        all_ships = []
        board_ships_coords = [] 

        print("\n🚢 Começando o posicionamento MANUAL dos seus barcos! 🚢")
        
        for size in ship_sizes:
            new_ship = get_ship_position(board_ships_coords, size, is_valid_placement_func)
            all_ships.append(new_ship)
            board_ships_coords.extend(new_ship)
            
        print("✅ Seu posicionamento manual concluído.")
        return all_ships


def get_shot(palpite):
 
    ok = "n"
    while ok == "n":
        try:
            tiro_input = input("🎯 Por favor, insira sua posição de tiro (0-99) ou [P] para pausar: ").strip().upper()
            
            if tiro_input == 'P':
                return 'PAUSE' 

            tiro = int(tiro_input)
            
            if tiro < 0 or tiro > 99:
                print("Entrada incorreta (fora do 0-99), tente novamente.")
            elif tiro in palpite:
                print("Você já atirou nessa posição. Tente novamente.")
            else:
                ok = "s"
                break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número ou 'P'.")
            log_erro("Valor inválido inserido em get_shot.")
    return tiro

def get_enemy_shot(enemy_shots):
   
    while True:
        tiro = random.randint(0, 99)
        if tiro not in enemy_shots:
            print(f"\n🤖 Inimigo atira em: {tiro}") 
            return tiro

def mostrar_tabuleiro(estado_do_jogo):
    
    
    hit_enemy = estado_do_jogo['hit_enemy']
    miss_enemy = estado_do_jogo['miss_enemy']
    afundou_enemy = estado_do_jogo['afundou_enemy']
    player_ship_coords = estado_do_jogo['player_ship_coords']
    hit_player = estado_do_jogo['hit_player']
    miss_player = estado_do_jogo['miss_player']
    afundou_player = estado_do_jogo['afundou_player']
    
    
    print("\n" + "=" * 55)
    print("     SEU TABULEIRO    🎭        |       🏴‍☠️   TABULEIRO INIMIGO     ")
    print("      0  1  2  3  4  5  6  7  8  9 |       0  1  2  3  4  5  6  7  8  9 ")
    print("=" * 55)

    player_ship_set = set(player_ship_coords)
    
    contador = 0
    for x in range(10): # gera as linhas
        linha_player = ""
        linha_enemy = ""

        for _ in range(10):
            # meu tabuleiro
            ch_p = " _ " 
            if contador in afundou_player:
                ch_p = " 💥" 
            elif contador in hit_player:
                ch_p = " O " 
            elif contador in player_ship_set:
                ch_p = " 🚢" 
            elif contador in miss_player:
                ch_p = " X " 

            linha_player += ch_p
            
            # tabuleiro inimigo
            ch_e = " _ "
            if contador in afundou_enemy:
                ch_e = " 💥" 
            elif contador in hit_enemy:
                ch_e = " O " 
            elif contador in miss_enemy:
                ch_e = " X " 

            linha_enemy += ch_e
            contador += 1
            
        print(f"{x}  {linha_player} | {x}   {linha_enemy}")
    print("-" * 55)




def mostrar_creditos():
    print("\n" + "=" * 40)
    print("           CRÉDITOS E VERSÃO          ")
    print("=" * 40)
    print("🚀 Batalha Naval em Console - Versão 1.0")
    print("\nDesenvolvido por: Rebeca Dias")
    print("Disciplina: Algoritmos Computacionais - Engenharia Elétrica")
    print("Universidade do Estado do Rio de Janeiro - UERJ")
    print("Professor: Gabriel C. de Carvalho")
    print("\nFuturas features planejadas ( se eu estiver com tempo e sabedoria ): Menu de Configurações, Argumentos de Console.")
    print("-" * 40)
    input("\nPressione Enter para voltar ao Menu Principal...")

def mostrar_menu_principal():
    
    


    print("\n" + "=" * 30)
    print("---🏴‍☠️ Batalha Naval em Python 🏴‍☠️---")
    print("=" * 30)
    
    print("1. Iniciar Novo Jogo")
    print("2. Carregar Jogo")
    print("3. Ver Regras")
    print("4. Histórico de Partidas")
    print("5. Créditos")
    print("6. Configurações") 
    print("-" * 30)
    
    while True:
        escolha = input("Escolha uma opção: ")
        if escolha in ['1', '2', '3', '4', '5', '6', '7']: 
            return escolha
        print("Opção inválida. Tente novamente.")

def mostrar_menu_pause():

    print("\n" + "=" * 30)
    print("         MENU DE PAUSE        ")
    print("=" * 30)
    print("1. Iniciar Novo Jogo (Sem salvar)")
    print("2. Carregar Partida (Sem salvar a atual)")
    print("3. Salvar Partida em Arquivo")
    print("4. Voltar para o Jogo")
    print("5. Voltar ao Menu Principal (Sem salvar)")
    print("6. Sair do Jogo")
    print("-" * 30)
    
    while True:
        escolha = input("Escolha uma opção (1-6): ")
        if escolha in ['1', '2', '3', '4', '5', '6']:
            return escolha
        print("Opção inválida. Escolha 1-6.")

def mostrar_menu_arquivos(acao="salvar"):
 
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    
    arquivos_existentes = [f.replace('.save', '') for f in os.listdir(SAVE_FOLDER) if f.endswith('.save')]
    
    print("\n" + "=" * 40)
    print(f"        MENU DE ARQUIVOS ({acao.upper()})      ")
    print("=" * 40)
    print(f"Arquivos existentes ({SAVE_FOLDER}/):")
    
    if arquivos_existentes:
        for i, nome in enumerate(arquivos_existentes):
            print(f" {i+1}. {nome}")
    else:
        print(" (Nenhum arquivo de save encontrado)")
        
    print("\n[V] Voltar ao menu anterior.")
    
    while True:
        if acao == "salvar":
            prompt = "Digite o nome para o NOVO SAVE ou o número para SOBRESCREVER: "
        else:
            prompt = "Digite o número do arquivo para CARREGAR: "
            
        escolha = input(prompt).strip()
        
        if escolha.upper() == 'V':
            return 'VOLTAR'

        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(arquivos_existentes):
                return arquivos_existentes[indice]
        except ValueError:
            pass
            
        if acao == "salvar" and escolha:
            if escolha in arquivos_existentes:
                confirma = input(f"AVISO: O arquivo '{escolha}.save' será SOBRESCRITO. Confirmar? (s/n): ").strip().lower()
                if confirma != 's':
                    continue 
            return escolha
            
        print("Escolha inválida.")

def mostrar_regras():
    
    print("\n" + "=" * 30)
    print("          REGRAS DO JOGO      ")
    print("=" * 30)
    print("1. O tabuleiro é 10x10 (coordenadas 0-99).")
    print("2. Cada jogador possui 3 navios: Tamanhos 4, 3 e 2.")
    print("3. Os barcos não podem se sobrepor ou sair do tabuleiro.")
    print("4. O jogo é jogado em turnos de 5 tiros alternados.")
    print("5. Você vence ao destruir todos os 9 segmentos de navio inimigos.")
    print("6. Você perde se o inimigo destruir todos os seus 9 segmentos de navio.")
    input("\nPressione Enter para voltar ao Menu Principal...")

def mostrar_historico():
   
    
    if not os.path.exists(SAVE_FOLDER): 
        os.makedirs(SAVE_FOLDER)
        
    print("\n" + "=" * 30)
    print("       HISTÓRICO DE PARTIDAS  ")
    print("=" * 30)
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            conteudo = f.read()
            if conteudo:
                print(conteudo)
            else:
                print("Nenhum registro de partida encontrado.")
    except FileNotFoundError:
        print("Nenhum arquivo de histórico encontrado.")
    except Exception as e:
        log_erro(f"Erro ao ler histórico: {e}")
        print("Erro ao ler o histórico.")
        
    input("\nPressione Enter para voltar ao Menu Principal...")