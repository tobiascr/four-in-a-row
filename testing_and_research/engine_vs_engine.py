
from engine1 import EngineInterface as EngineInterface1
from engine1 import GameState as GameState1
from engine2 import EngineInterface as EngineInterface2
from engine2 import GameState as GameState2
import time

engine_interface_1 = EngineInterface1(2)
engine_interface_1.name = "engine1"
engine_interface_2 = EngineInterface2(2)
engine_interface_2.name = "engine2"

def game(engine1, game_state1, engine2, game_state2, print_move_times=False):
    """engine1 and engine2 are instances of EngineInterface.
    engine1 makes the first move.
    Return 0 if the result is a draw, 1 if engine1 win and 2 if engine2 win.
    """
    def print_total_times():
        print(engine1.name + " total time:", total_time_engine_1)
        print(engine2.name + " total time:", total_time_engine_2)
    
    total_time_engine_1 = 0
    total_time_engine_2 = 0    
    while True:
        t0 = time.clock()
        column_number = engine1.engine_move(game_state1)
        t1 = time.clock()
        total_time_engine_1 += t1 - t0
        if print_move_times:
            print(engine1.name + ": Move time:", t1 - t0, "s")            
        game_state1.make_move(column_number)
        game_state2.make_move(column_number)
        if engine1.four_in_a_row(game_state1):
            print_total_times()
            print(engine1.name + " wins" + "\n")
            return 1
        if game_state1.number_of_moves == 42:
            print_total_times()        
            print("Draw\n")        
            return 0
        t0 = time.clock()
        column_number = engine2.engine_move(game_state2)
        t1 = time.clock()
        total_time_engine_2 += t1 - t0        
        if print_move_times:
            print(engine2.name + ": Move time:", t1 - t0, "s")
        game_state1.make_move(column_number)
        game_state2.make_move(column_number)        
        if engine2.four_in_a_row(game_state2):
            print_total_times()        
            print(engine2.name + " wins" + "\n")
            return 2
        if game_state2.number_of_moves == 42:
            print_total_times()
            print("Draw\n")
            return 0
            
def games(engine1, engine2, number_of_games, print_move_times=False):
    """Let engine1 and engine2 play several games against each other.
    Each begin every second game."""
    engine1_wins = 0
    engine2_wins = 0
    draws = 0
    for n in range(1, number_of_games + 1):
        print("Game", n)
        if n % 2:
            game_state1 = GameState1()
            game_state2 = GameState2()        
            result = game(engine1, game_state1, engine2, game_state2, print_move_times)
            if result == 1:
                engine1_wins += 1
            elif result == 2:
                engine2_wins += 1
            else:
                draws += 1
        else:
            game_state1 = GameState1()
            game_state2 = GameState2()        
            result = game(engine2, game_state2, engine1, game_state1, print_move_times)
            if result == 1:
                engine2_wins += 1
            elif result == 2:
                engine1_wins += 1
            else:
                draws += 1
    return (engine1.name + " wins: " + str(engine1_wins) + 
            "\n" + engine2.name + " wins: " + str(engine2_wins) + "\ndraws: " + str(draws))

print(games(engine_interface_1, engine_interface_2, 10, True))
