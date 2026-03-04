import random



def is_valid_ship_placement(board_ships, start, length, direction):
    
    
    increment = 0
    if direction == 'h': # Horizontal (coluna muda: +1)
        increment = 1
        if (start // 10) != ((start + length - 1) // 10):
            return False, []
            
    elif direction == 'v': # Vertical (linha muda: +10)
        increment = 10
        if start + (length - 1) * 10 > 99:
            return False, []
            
    else:
        return False, []

    ship_coords = []
    for i in range(length):
        current_pos = start + i * increment
        
        if not (0 <= current_pos <= 99):
            return False, []
        
        if current_pos in board_ships:
            return False, []
            
        ship_coords.append(current_pos)

    return True, ship_coords

def get_ship_position(board_ships, ship_size):
   
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
            
            is_valid, ship_coords = is_valid_ship_placement(board_ships, start, ship_size, direction)

            if is_valid:
                return ship_coords
            else:
                print("Colocação inválida! O barco sai do tabuleiro ou colide com outro. Tente novamente.")

        except ValueError:
            print("Entrada inválida. Por favor, insira um número para a posição.")

def get_random_ship_position(board_ships, ship_size):
   
    while True:
        start = random.randint(0, 99)
        direction = random.choice(['h', 'v'])
        
        is_valid, ship_coords = is_valid_ship_placement(board_ships, start, ship_size, direction)

        if is_valid:
            return ship_coords
            

def setup_player_ships_manual():
    
    ship_sizes = [4, 3, 2] 
    all_ships = []
    board_ships_coords = [] # Coordenadas ocupadas

    print("🚢 Começando o posicionamento dos seus barcos! 🚢")
    
    for size in ship_sizes:
       
        new_ship = get_ship_position(board_ships_coords, size)
                
        all_ships.append(new_ship)
        board_ships_coords.extend(new_ship)
        
    print("✅ Seu posicionamento concluído.")
    return all_ships

def setup_enemy_ships_randomly():
    
    ship_sizes = [4, 3, 2] 
    all_ships = []
    board_ships = [] 

    print("🤖 Barcos Inimigos sendo posicionados aleatoriamente...")
    
    for size in ship_sizes:
       
        new_ship = get_random_ship_position(board_ships, size)
                
        all_ships.append(new_ship)
        board_ships.extend(new_ship)
        
    print("✅ Posicionamento do Inimigo concluído.")
    return all_ships



def get_shot(palpite):
  
    ok = "n"
    while ok == "n":
        try:
            tiro = int(input("🎯 Por favor, insira sua posição de tiro (0-99) no tabuleiro inimigo: "))
            if tiro < 0 or tiro > 99:
                print("Entrada incorreta (fora do 0-99), tente novamente.")
            elif tiro in palpite:
                print("Você já atirou nessa posição. Tente novamente.")
            else:
                ok = "s"
                break
        except ValueError:
            print("Por favor, insira um número.")
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
    print("     SEU TABULEIRO             |           TABULEIRO INIMIGO     ")
    print("      0  1  2  3  4  5  6  7  8  9 |       0  1  2  3  4  5  6  7  8  9 ")
    print("=" * 55)

    player_ship_set = set(player_ship_coords)
    
    contador = 0
    for x in range(10):  # gera as linhas
        linha_player = ""
        linha_enemy = ""

        for _ in range(10):
            # meu tabuleiro
            ch_p = " _ " 
            if contador in afundou_player:
                ch_p = " 💥" # Barco afundado pelo inimigo
            elif contador in hit_player:
                ch_p = " O " # Acerto do inimigo
            elif contador in player_ship_set:
                ch_p = " 🚢" # Seu barco (não atingido)
            elif contador in miss_player:
                ch_p = " X " # Erro do inimigo

            linha_player += ch_p
            
            # tabuleiro inimigo
            ch_e = " _ "
            if contador in afundou_enemy:
                ch_e = " 💥" # Afundou inimigo
            elif contador in hit_enemy:
                ch_e = " O " # Acertou inimigo
            elif contador in miss_enemy:
                ch_e = " X " # Errou inimigo

            linha_enemy += ch_e
            contador += 1
            
        print(f"{x}  {linha_player} | {x}   {linha_enemy}")
    print("-" * 55)
    
def verificar_tiro(estado_do_jogo, tiro, is_player_turn=True):

    if is_player_turn:
        ships = estado_do_jogo['enemy_ships_on_board']
        hit = estado_do_jogo['hit_enemy']
        miss = estado_do_jogo['miss_enemy']
        afundou = estado_do_jogo['afundou_enemy']
    else:
        ships = estado_do_jogo['player_ships_on_board']
        hit = estado_do_jogo['hit_player']
        miss = estado_do_jogo['miss_player']
        afundou = estado_do_jogo['afundou_player']
    
    acertou = False
    
    for barco in ships:
        if tiro in barco:
            acertou = True
            barco.remove(tiro)
            
            if len(barco) == 0:
                quem = "VOCÊ" if is_player_turn else "INIMIGO"
                print(f"🔥 O {quem} AFUNDOU UM BARCO INFIèL! 🔥")
                
                afundou.append(tiro) 
                if tiro in hit:
                     hit.remove(tiro)

            else:
                hit.append(tiro)
            
            break 
    
    if not acertou:
        miss.append(tiro)
        quem = "Você" if is_player_turn else "O inimigo"
        print(f"{quem} errou o tiro em {tiro}.")


    if is_player_turn:
        estado_do_jogo['total_len_enemy'] = sum(len(barco) for barco in ships)
    else:
        estado_do_jogo['total_len_player'] = sum(len(barco) for barco in ships)

    return estado_do_jogo



all_enemy_ships = setup_enemy_ships_randomly() 
all_player_ships = setup_player_ships_manual()


estado_do_jogo = {
    # Barcos em Jogo (listas mutáveis)
    'enemy_ships_on_board': [s[:] for s in all_enemy_ships], 
    'player_ships_on_board': [s[:] for s in all_player_ships],

    # coordenadas fixas do jogador para mostrar no tabuleiro)
    'player_ship_coords': [coord for ship in all_player_ships for coord in ship], 

    # rastreamento de Tiros do player no tabuleiro inimigo
    'hit_enemy': [], 
    'miss_enemy': [],
    'afundou_enemy': [],
    

    'hit_player': [],
    'miss_player': [],
    'afundou_player': [],

    
    'rodada': 0,

    'total_len_enemy': sum(len(barco) for barco in all_enemy_ships),
    'total_len_player': sum(len(barco) for barco in all_player_ships)
}



print("🔥 Todos os Barcos Posicionados. Que comece a batalha! 🔥")


rodada = 0
while rodada < 100:
    rodada += 1
    
    # Adicionamos uma checagem de vitória/derrota no topo do loop
    if estado_do_jogo['total_len_enemy'] == 0 or estado_do_jogo['total_len_player'] == 0:
        break

    print(f"\n======== RODADA {rodada} (5 TIROS PARA CADA) ========")
    
    
   
    print("\n--- SEU TURNO: 5 TIROS ---")

    for tiro_num in range(1,6):
        print(f"[Seu Tiro {tiro_num} de 5]") 

       
        mostrar_tabuleiro(estado_do_jogo) 
    
        
        palpite_enemy = estado_do_jogo['hit_enemy'] + estado_do_jogo['miss_enemy'] + estado_do_jogo['afundou_enemy']
        tiro_jogador = get_shot(palpite_enemy)
    
    
        estado_do_jogo = verificar_tiro(estado_do_jogo, tiro_jogador, is_player_turn=True)  # chama a verificação e atualiza o dicionário (retorna o próprio dicionário)

       
        if estado_do_jogo['total_len_enemy'] == 0:   # checa a vitória usando a chave do dicionário
            mostrar_tabuleiro(estado_do_jogo)
            print("🎉 VITÓRIA!! Todos os infiéis inimigos foram afundados. ♨️ ")
            break 
        
        print(f"Posições de barcos inimigos restantes: {estado_do_jogo['total_len_enemy']} ")

    if estado_do_jogo['total_len_enemy'] == 0:
        continue 

    
    
    print("--- TURNO DO INIMIGO : 5 TIROS---")

    for tiro_num in range(1,6):
        
        # Obtém o palpite de tiro do inimigo
        palpite_player = estado_do_jogo['hit_player'] + estado_do_jogo['miss_player'] + estado_do_jogo['afundou_player'] 
        tiro_inimigo = get_enemy_shot(palpite_player)
        
        print(f"[Tiro inimigo {tiro_num} de 5. ]")

        # Chama a verificação e atualiza o dicionário
        estado_do_jogo = verificar_tiro(estado_do_jogo, tiro_inimigo, is_player_turn=False)

        # Checa a derrota usando a chave do dicionário
        if estado_do_jogo['total_len_player'] == 0:
            mostrar_tabuleiro(estado_do_jogo)
            print("😭 DERROTA TOTAL, PÂNICO! Todos os seus barcos foram afundados pelo inimigo. ⚠️⚠️")
            break 

        print(f"Suas posições de barcos restantes: {estado_do_jogo['total_len_player']}")

    # Checa a derrota para forçar o fim do loop principal na próxima iteração
    if estado_do_jogo['total_len_player'] == 0:
        continue

# Quando o loop termina (seja por vitória, derrota ou limite de rodadas)
if rodada == 100:
    print("FIM DE JOGO: Você atingiu o limite de rodadas. ⚠️ ")
    
print("\n--- ESTATÍSTICAS FINAIS ---")
mostrar_tabuleiro(estado_do_jogo)