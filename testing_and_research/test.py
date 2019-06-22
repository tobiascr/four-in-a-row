import four_in_a_row_command_line
import time

def computer_move_test(game_state, depth):
    neutral_moves = []
    best_value = -10000 * game_state.player_in_turn
    available_moves = game_state.available_moves()
    for move in available_moves:        
        game_state.make_move(move)               
        value = four_in_a_row_command_line.minimax_value(game_state, depth)
        game_state.undo_last_move()
        if value == 0:
            neutral_moves.append(move)
        # If maximizing player.         
        if game_state.player_in_turn == 1:
            if value > best_value:
                best_value = value
                best_move = move
        # If minimizing player.
        else:
            if value < best_value:
                best_value = value
                best_move = move
                
    # If 0 is the best rating, then make a heuristic choise among the 0-rated moves.
    if best_value == 0:
       best_value = -10000
       for move in neutral_moves:
           value = four_in_a_row_command_line.heuristic_value_random(game_state, move)
           if value > best_value:
               best_value = value
               best_move = move
                              
    return best_move
    
def make_move_algorithm_1(game_state):
    #move = four_in_a_row_command_line.random_move(game_state)
    move = computer_move_test(game_state, 3)
    
    game_state.make_move(move)

def make_move_algorithm_2(game_state):
    move = four_in_a_row_command_line.computer_move(game_state)
    game_state.make_move(move)

def game_algorithm_1_vs_algorithm_2():
    """This function lets algorithms 1 and 2 play a game with each other."""
    
    game_state = four_in_a_row_command_line.GameState()
    
    while True:
        make_move_algorithm_1(game_state)
        if four_in_a_row_command_line.win_last_move(game_state):
            result = "Algorithm 1 win"
            break
        elif game_state.number_of_moves == 42:
            result = "Draw"
            break
            
        make_move_algorithm_2(game_state)
        if four_in_a_row_command_line.win_last_move(game_state):
            result = "Algorithm 2 win"
            break
        elif game_state.number_of_moves == 42:
            result = "Draw"
            break        
            
    return result

win_1 = 0
win_2 = 0
draws = 0

t0 = time.perf_counter()

for i in range(100):
    result = game_algorithm_1_vs_algorithm_2()
    t = time.perf_counter()
    print(result, t-t0)
    t0 = t
    if result == "Algorithm 1 win":
        win_1 += 1
    if result == "Algorithm 2 win":
        win_2 += 1
    if result == "Draw":
        draws += 1

print()
print("Algorithm 1 win:", win_1)
print("Algorithm 2 win:", win_2)
print("Draws:", draws)
