
from engine import EngineInterface as EngineInterface1
from test_engine import EngineInterface as EngineInterface2
import time

engine_interface_1 = EngineInterface1(3)
engine_interface_1.name = "engine"
engine_interface_2 = EngineInterface2(3)
engine_interface_2.name = "test_engine"

def game(engine1, engine2, print_move_times=False):
    """engine1 and engine2 are instances of EngineInterface.
    engine1 makes the first move.
    Return (result, engine1 time, engine2 time)
    result is 0 if the game is a draw, 1 if engine1 win and 2 if engine2 win.
    """
    def print_total_times():
        print(engine1.name + " total time:", total_time_engine_1)
        print(engine2.name + " total time:", total_time_engine_2)

    total_time_engine_1 = 0
    total_time_engine_2 = 0
    while True:
        t0 = time.perf_counter()
        column_number = engine1.engine_move()
        t1 = time.perf_counter()
        total_time_engine_1 += t1 - t0
        if print_move_times:
            print(engine1.name + ": Move time:", t1 - t0, "s")
        engine1.make_move(column_number)
        engine2.make_move(column_number)
        if engine1.four_in_a_row():
            print_total_times()
            print(engine1.name + " wins" + "\n")
            return (1, total_time_engine_1, total_time_engine_2)
        if engine1.draw():
            print_total_times()
            print("Draw\n")
            return (0, total_time_engine_1, total_time_engine_2)
        t0 = time.perf_counter()
        column_number = engine2.engine_move()
        t1 = time.perf_counter()
        total_time_engine_2 += t1 - t0
        if print_move_times:
            print(engine2.name + ": Move time:", t1 - t0, "s")
        engine1.make_move(column_number)
        engine2.make_move(column_number)
        if engine2.four_in_a_row():
            print_total_times()
            print(engine2.name + " wins" + "\n")
            return (2, total_time_engine_1, total_time_engine_2)
        if engine2.draw():
            print_total_times()
            print("Draw\n")
            return (0, total_time_engine_1, total_time_engine_2)

def games(engine1, engine2, number_of_games, print_move_times=False):
    """Let engine1 and engine2 play several games against each other.
    Each begin every second game."""
    engine1_wins = 0
    engine2_wins = 0
    engine1_time = 0
    engine2_time = 0

    draws = 0
    for n in range(1, number_of_games + 1):
        print("Game", n)
        engine_interface_1.new_game()
        engine_interface_2.new_game()
        if n % 2:
            (result, t1, t2) = game(engine1, engine2, print_move_times)
            if result == 1:
                engine1_wins += 1
            elif result == 2:
                engine2_wins += 1
            else:
                draws += 1
            engine1_time += t1
            engine2_time += t2
        else:
            (result, t2, t1) = game(engine2, engine1, print_move_times)
            if result == 1:
                engine2_wins += 1
            elif result == 2:
                engine1_wins += 1
            else:
                draws += 1
            engine1_time += t1
            engine2_time += t2
    print(engine1.name + " wins: " + str(engine1_wins) + 
          "\n" + engine2.name + " wins: " + str(engine2_wins) + "\ndraws: " + str(draws))
    print(engine1.name + " total time:", engine1_time, "s")
    print(engine2.name + " total time:", engine2_time, "s")

games(engine_interface_1, engine_interface_2, 100, False)
