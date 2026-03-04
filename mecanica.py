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

def setup_ships_randomly(): 
 
    ship_sizes = [4, 3, 2] 
    all_ships = []
    board_ships = [] 
    
    for size in ship_sizes:
        while True:
            start = random.randint(0, 99)
            direction = random.choice(['h', 'v'])
            is_valid, new_ship = is_valid_ship_placement(board_ships, start, size, direction)
            if is_valid:
                break
                
        all_ships.append(new_ship)
        board_ships.extend(new_ship)
        
    return all_ships


def verificar_tiro(estado_do_jogo, tiro, is_player_turn=True):

    
    if is_player_turn:
        ships = estado_do_jogo['enemy_ships_on_board']
        hit = estado_do_jogo['hit_enemy']
        miss = estado_do_jogo['miss_enemy']
        afundou = estado_do_jogo['afundou_enemy']
        len_key = 'total_len_enemy'
    else:
        ships = estado_do_jogo['player_ships_on_board']
        hit = estado_do_jogo['hit_player']
        miss = estado_do_jogo['miss_player']
        afundou = estado_do_jogo['afundou_player']
        len_key = 'total_len_player'
    
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

    estado_do_jogo[len_key] = sum(len(barco) for barco in ships) 

    return estado_do_jogo