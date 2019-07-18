
from engine_copy import EngineInterface as EngineInterface1
from engine_test import EngineInterface as EngineInterface2
from engine_copy import GameState

engine_interface_1 = EngineInterface2(1)
engine_interface_2 = EngineInterface2(2)

def game(engine1, engine2):
    """engine1 and engine2 are instances of EngineInterface.
    engine1 makes the first move.
    Return 0 if the result is a draw, 1 if engine1 win and 2 if engine2 win.
    """
    game_state = GameState()
    while True:        
        column_number = engine1.engine_move(game_state)
        game_state.make_move(column_number)                
        if engine1.four_in_a_row(game_state):
            return 1
        if game_state.number_of_moves == 42:
            return 0                                    
        column_number = engine2.engine_move(game_state)
        game_state.make_move(column_number)
        if engine2.four_in_a_row(game_state):
            return 2
        if game_state.number_of_moves == 42:
            return 0
            
def games(engine1, engine2, number_of_games):
    """Let engine1 and engine2 play several games against each other.
    Each begin every second game."""
    engine1_wins = 0
    engine2_wins = 0
    draws = 0
    for n in range(number_of_games):
        print(n)
        if n % 2:
            result = game(engine1, engine2)           
            if result == 1:
                engine1_wins += 1
            elif result == 2:
                engine2_wins += 1
            else:
                draws += 1
        else:
            result = game(engine2, engine1)
            if result == 1:
                engine2_wins += 1
            elif result == 2:
                engine1_wins += 1
            else:
                draws += 1
    return ("engine1 wins: " + str(engine1_wins) +
            " engine2 wins: " + str(engine2_wins) + " draws: " + str(draws))

print(games(engine_interface_1, engine_interface_2, 20))

            
            
