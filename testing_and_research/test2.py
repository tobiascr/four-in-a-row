
import engine
import version1dot0_four_in_a_row_command_line as version_1_engine
import time

depth = 7

def test_version_1_engine():
    game_state = version_1_engine.GameState()
    game_state.make_move(3)
    game_state.make_move(3)
    game_state.make_move(3)
    game_state.make_move(2)
    game_state.make_move(2)
    game_state.make_move(2)
    game_state.make_move(3)
    game_state.make_move(3)       
    t0 = time.perf_counter()
    value = version_1_engine.minimax_value(game_state, depth)
    t1 = time.perf_counter()
    print("version_1_engine. value:", value, "time:", t1-t0)

def test_engine():
    game_state = engine.GameState()
    game_state.make_move(3)
    game_state.make_move(3)
    game_state.make_move(3)
    game_state.make_move(2)
    game_state.make_move(2)
    game_state.make_move(2)
    game_state.make_move(3)
    game_state.make_move(3)    
    t0 = time.perf_counter()
    value = engine.minimax_value(game_state, depth)
    t1 = time.perf_counter()
    print("engine. value:", value, "time:", t1-t0)
    
test_engine()    
#test_version_1_engine()
