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

def mostrar_tabuleiro(hit_enemy, miss_enemy, afundou_enemy, player_ships_coords, hit_player, miss_player, afundou_player):
   
    
    print("\n" + "=" * 55)
    print("     SEU TABULEIRO             |           TABULEIRO INIMIGO     ")
    print("      0  1  2  3  4  5  6  7  8  9 |       0  1  2  3  4  5  6  7  8  9 ")
    print("=" * 55)

    player_ship_set = set(player_ships_coords)
    
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
    
def verificar_tiro(ships, hit, miss, afundou, tiro, is_player_turn=True):
    
    acertou = False
    
    for barco in ships:
        if tiro in barco:
            acertou = True
            barco.remove(tiro)
            
            if len(barco) == 0:
                quem = "VOCÊ" if is_player_turn else "INIMIGO"
                print(f"🔥 O {quem} AFUNDOU UM BARCO! 🔥")
                
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

    return ships, hit, miss, afundou



all_enemy_ships = setup_enemy_ships_randomly() 
all_player_ships = setup_player_ships_manual()

# Barcos ativos 
enemy_ships_on_board = [s[:] for s in all_enemy_ships] 
player_ships_on_board = [s[:] for s in all_player_ships]
player_ship_coords = [coord for ship in all_player_ships for coord in ship] # Coordenadas de todos os navios do jogador para exibir

print("🔥 Todos os Barcos Posicionados. Que comece a batalha! 🔥")

# Variáveis de estado para o Inimigo (tiros do jogador)
hit_enemy = [] 
miss_enemy = []
afundou_enemy = []
palpite_enemy = [] # Todos os tiros dados pelo jogador

# Variáveis de estado para o Jogador (tiros do inimigo)
hit_player = []
miss_player = []
afundou_player = []
palpite_player = [] # Todos os tiros dados pelo inimigo

total_len_enemy = sum(len(barco) for barco in enemy_ships_on_board)
total_len_player = sum(len(barco) for barco in player_ships_on_board)

rodada = 0

# O loop principal agora só checa o limite de rodadas. 
# A condição de vitória/derrota é checada e forçada DENTRO dos turnos.
while rodada < 100:
    rodada += 1
    
    # Adicionamos uma checagem de vitória/derrota no topo do loop
    if total_len_enemy == 0 or total_len_player == 0:
        break

    print(f"\n======== RODADA {rodada} (5 TIROS PARA CADA) ========")
    
    
    # --- TURNO DO JOGADOR (5 TIROS) ---
    print("\n--- SEU TURNO: 5 TIROS ---")

    for tiro_num in range(1,6):
        print(f"[Seu Tiro {tiro_num} de 5]") 

        mostrar_tabuleiro(hit_enemy, miss_enemy, afundou_enemy, player_ship_coords, hit_player, miss_player, afundou_player) 
    
        palpite_enemy = hit_enemy + miss_enemy + afundou_enemy
        tiro_jogador = get_shot(palpite_enemy)
    
        enemy_ships_on_board, hit_enemy, miss_enemy, afundou_enemy = verificar_tiro(enemy_ships_on_board, hit_enemy, miss_enemy, afundou_enemy, tiro_jogador, is_player_turn=True)

        total_len_enemy = sum(len(barco) for barco in enemy_ships_on_board)

        if total_len_enemy == 0:
            mostrar_tabuleiro(hit_enemy, miss_enemy, afundou_enemy, player_ship_coords, hit_player, miss_player, afundou_player)
            print("🎉 VITÓRIA!! Todos os barcos inimigos foram afundados. ♨️ ")
            # CORREÇÃO CHAVE: Aqui, só saímos do loop de 5 tiros.
            break 
        
        print(f"Posições de barcos inimigos restantes: {total_len_enemy} ")


    # CORREÇÃO CHAVE: Se a vitória ocorreu, usamos 'continue' para pular o resto da rodada (turno do inimigo)
    # e voltar ao topo do while, onde o break será ativado
    if total_len_enemy == 0:
        continue # Pula o turno do inimigo e volta ao início do while

    
    # --- TURNO DO INIMIGO (5 TIROS) ---
    print("\n--- TURNO DO INIMIGO : 5 TIROS---")

    for tiro_num in range(1,6):
        
        palpite_player = hit_player + miss_player + afundou_player 
        tiro_inimigo = get_enemy_shot(palpite_player)
        
        print(f"[Tiro inimigo {tiro_num} de 5. ]")

        player_ships_on_board, hit_player, miss_player, afundou_player = verificar_tiro(player_ships_on_board, hit_player, miss_player, afundou_player, tiro_inimigo, is_player_turn=False)

        total_len_player = sum(len(barco) for barco in player_ships_on_board)

        if total_len_player == 0:
            mostrar_tabuleiro(hit_enemy, miss_enemy, afundou_enemy, player_ship_coords, hit_player, miss_player, afundou_player)
            print("😭 DERROTA TOTAL, PÂNICO! Todos os seus barcos foram afundados pelo inimigo. ⚠️⚠️")
            # CORREÇÃO CHAVE: Aqui, só saímos do loop de 5 tiros.
            break 

        print(f"Suas posições de barcos restantes: {total_len_player}")

    # Checa a derrota (vitória do inimigo) para forçar o fim do loop principal na próxima iteração
    if total_len_player == 0:
        continue # Volta ao topo do while e ativa o break de saída

# Quando o loop termina (seja por vitória, derrota ou limite de rodadas)
if rodada == 100:
    print("FIM DE JOGO: Você atingiu o limite de rodadas. ⚠️ ")
    
print("\n--- ESTATÍSTICAS FINAIS ---")
mostrar_tabuleiro(hit_enemy, miss_enemy, afundou_enemy, player_ship_coords, hit_player, miss_player, afundou_player)