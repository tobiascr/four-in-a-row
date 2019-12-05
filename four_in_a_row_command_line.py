
from engine import EngineInterface
from engine import GameState

def draw_board(game_state, white):
    """White (1 or -1) tells which of 1 and -1 that is drawn in white color.
    game_state is an instance of GameState.
    """
    for row in range(6):
        for col in range(7):
            print("|", end="")
            if game_state.get_value(col, 5-row) == "0":
                print(" ", end="")
            else:
                if white:
                    if game_state.get_value(col, 5-row) == "1":
                        print("○", end="")
                    else:
                        print("●", end="")
                else:
                    if game_state.get_value(col, 5-row) == "2":
                        print("○", end="")
                    else:
                        print("●", end="")
        print("|")
    print(" 0 1 2 3 4 5 6")

if __name__ == "__main__":

    new_game = True
    computer_begin = False

    print()
    print("Type 0 to 6 to make a move. Type q to quit.")
    print()

    while True:
        answer = input("Difficulty level (1-3): ")
        if answer == "1" or answer == "2" or answer == "3":
            difficulty = int(answer)
            engine_interface = EngineInterface(difficulty)
            print()
            break
        elif answer == "q":
            exit_program = True
            break

    while True:
        if new_game:
            game_state = GameState()
            player_win = False
            computer_win = False
            computer_in_turn = computer_begin
            if computer_begin:
                computer_number = 1
            else:
                computer_number = -1
                draw_board(game_state, 1) # Draws an empty board.
                print()

            computer_begin = not computer_begin
            new_game = False

        if computer_in_turn:
            # Computer makes a move
            move = engine_interface.engine_move(game_state)
            game_state.make_move(move)
            if engine_interface.four_in_a_row(game_state):
                computer_win = True
        else:
            # Player makes a move
            while True:
                move_str = input("Input: ")
                if move_str in "0123456q" and len(move_str) == 1:
                    if move_str == "q":
                        break
                    else:
                        move = int(move_str)
                    if game_state.column_height[move] < 6:
                        game_state.make_move(move)
                        if engine_interface.four_in_a_row(game_state):
                            player_win = True
                        print()
                        break
 
        if move_str == "q":
            break

        if computer_in_turn or player_win or game_state.number_of_moves == 42:
            draw_board(game_state, -computer_number)
            print()

        computer_in_turn = not computer_in_turn

        if player_win:
            print("Player wins. Congratulations!")
        elif computer_win:
            print("Computer wins. Congratulations!")
        elif game_state.number_of_moves == 42:
            print("Draw")

        if player_win or computer_win or game_state.number_of_moves == 42:
            choise = ""
            while choise != "y" and choise != "n":
                print()
                choise = input("Play again (y/n)? ")
            if choise == "y":
                new_game = True
                print()
            if choise == "n": break

