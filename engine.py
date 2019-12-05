import random


class EngineInterface():
    """This class and the GameState class is intended to be the interface for this module.
    """
    def __init__(self, difficulty_level):
        """difficulty_level can be 1, 2 or 3."""
        self.difficulty_level = difficulty_level

    def four_in_a_row(self, game_state):
        """Return true if and only the last move made four in a row."""
        return win_last_move(game_state)

    def four_in_a_row_positions(self, game_state):
        """Return all positions on the board that have disks included in a four in a row.
        Positions are given as a set of (column, row)-pairs.
        """
        def disk_type(column, row):
            return game_state.board[10 + column + row * 9]

        def disks_are_of_same_type(col_row_pair_set):
            type_ = None
            all_equal = True
            for (column, row) in col_row_pair_set:
                if type_ == None:
                    type_ = disk_type(column, row)
                if type_ == "0":
                    return False
                if disk_type(column, row) != type_:
                    all_equal = False
            return all_equal

        possible_four_in_a_rows = []

        # Columns.
        for col in range(7):
            for row in range(3):
                col_row_pair_set = {(col, row), (col, row + 1),
                                    (col, row + 2), (col, row + 3)}
                possible_four_in_a_rows.append(col_row_pair_set)

        # Rows.
        for col in range(4):
            for row in range(6):
                col_row_pair_set = {(col, row), (col + 1, row),
                                    (col + 2, row), (col + 3, row)}
                possible_four_in_a_rows.append(col_row_pair_set)

        # Diagonals.
        for col in range(4):
            for row in range(3):
                col_row_pair_set = {(col, row), (col + 1, row + 1),
                                    (col + 2, row + 2), (col + 3, row + 3)}
                possible_four_in_a_rows.append(col_row_pair_set)

                col_row_pair_set = {(col, row + 3), (col + 1, row + 2),
                                    (col + 2, row + 1), (col + 3, row)}
                possible_four_in_a_rows.append(col_row_pair_set)

        four_in_a_rows = set()
        for col_row_pair_set in possible_four_in_a_rows:
            if disks_are_of_same_type(col_row_pair_set):
                four_in_a_rows |= col_row_pair_set

        return four_in_a_rows

    def engine_move(self, game_state):
        """Return an integer from 0 to 6 that represents a move made
        by the engine."""
        if self.difficulty_level == 1:
            return computer_move_level_1(game_state)
        if self.difficulty_level == 2:
            return computer_move_level_2(game_state)
        if self.difficulty_level == 3:
            return computer_move_level_3(game_state)


class GameState:
    """Instances of this object stores game states. A board configuration is stored as
    a list of lengths 72. Empty positions are stored as "0". The players are called "1" and "2",
    where "1" always make the first move.

    Some of the entries in the list is always 0. They represent the positions outside of the
    board, as in the following diagram.

    000000000
    0xxxxxxx0
    0xxxxxxx0
    0xxxxxxx0
    0xxxxxxx0
    0xxxxxxx0
    0xxxxxxx0
    000000000

    The positions with x are the positions on the board. The position in the lower left
    corner have index 10, the next index 11 etc.

    Many times in this program, rows and columns are refered to. Rows are counted from
    below and numbered 0, 1, ..., 5. Columns are counted from the left and are numbered
    0, 1, ..., 6. Moves are represented by the corresponding columns the moves are made to.
    """
    def __init__(self):
        self.number_of_moves = 0
        self.column_height = [0,0,0,0,0,0,0]
        self.move_history = []
        self.player_in_turn = "1"
        self.board = ["0"]*72

    def get_value(self, column, row):
        return self.board[10 + column + row * 9]

    def available_moves(self):
        return [move for move in range(7) if self.column_height[move] < 6]

    def make_move(self, column):
        self.board[10 + column + self.column_height[column] * 9] = self.player_in_turn
        self.move_history.append(column)
        self.column_height[column] += 1
        if self.player_in_turn == "1":
             self.player_in_turn = "2"
        else:
            self.player_in_turn = "1"
        self.number_of_moves += 1

    def undo_last_move(self):
        #last_move = self.move_sequence[-1]
        last_move = self.move_history.pop()
        self.column_height[last_move] -= 1
        self.board[10 + last_move + self.column_height[last_move] * 9] = "0"
        #del self.move_sequence[-1]
        if self.player_in_turn == "1":
             self.player_in_turn = "2"
        else:
            self.player_in_turn = "1"
        self.number_of_moves -= 1

    def key(self):
        """Return a unique key for the position that can be used in a dictionary."""
        return "".join(self.board)

def four_in_a_row(game_state, col, row):
    """True iff there is a four in a row that includes the position (col, row)."""
    position = 10 + col + row * 9
    player = game_state.board[position]

    # Columns.
    if row > 2:
        in_row = 1
        p = position - 9
        while game_state.board[p] == player:
            in_row += 1
            p -= 9
        if in_row >= 4:
            return True

    # Rows
    in_row = 1
    p = position - 1
    while game_state.board[p] == player:
        in_row += 1
        p -= 1
    p = position + 1
    while game_state.board[p] == player:
        in_row += 1
        p += 1
    if in_row >= 4:
        return True

    # Diagonals
    in_row = 1
    p = position - 10
    while game_state.board[p] == player:
        in_row += 1
        p -= 10
    p = position + 10
    while game_state.board[p] == player:
        in_row += 1
        p += 10
    if in_row >= 4:
        return True

    in_row = 1
    p = position - 8
    while game_state.board[p] == player:
        in_row += 1
        p -= 8
    p = position + 8
    while game_state.board[p] == player:
        in_row += 1
        p += 8
    if in_row >= 4:
        return True

    return False

def win_last_move(game_state):
    """True iff the last move made gives four in a row."""
    col = game_state.move_history[-1]
    row = game_state.column_height[col] - 1
    return four_in_a_row(game_state, col, row)

def heuristic_function_constant(game_state, move):
    return 0

def heuristic_function_1(game_state, move):
    """Give a heuristic evaluation in form of a number
    of how good it would be to make "move" to "game_state". The value is
    higher the better the move, regardless of the player to make it.

    This function give higher values to more central columns.
    """
    return -abs(3 - move)

def heuristic_function_3(game_state, move):
    """Give a heuristic evaluation in form of a number
    of how good it would be to make "move" to "game_state". The value is
    higher the better the move, regardless of the player to make it.

    This function give higher values to more central columns and rows.
    Tests shows that this function is stronger than the above heuristic functions.
    """
    row = game_state.column_height[move]
    return -abs(3 - move) - abs(2.5 - row)

def heuristic_function_4(game_state, move):
    """Give a heuristic evaluation in form of a number
    of how good it would be to make "move" to "game_state". The value is
    higher the better the move, regardless of the player to make it.

    This function give higher values to more central positions.
    """
    row = game_state.column_height[move]
    values = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 0],
              [0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]
    return values[row][move]

def heuristic_move(game_state, move_list, heuristic_function):
    """Return a move from move_list that is given the highest value by
    heuristic_function. It there are several such moves, then one of
    them are chosen randomly.
    """
    heuristic_values = [heuristic_function(game_state, move) for move in move_list]
    max_value = max(heuristic_values)
    best_moves = []
    for i in range(len(move_list)):
        if heuristic_values[i] == max_value:
            best_moves.append(move_list[i])
    return random.choice(best_moves)

def blocking_moves(game_state):
    """Return a list of moves that blocks an immediate four in a row for the opponent if
    such move exists.
    """
    move_list = []
    for col in game_state.available_moves():
        row = game_state.column_height[col]

        # Make a null move
        if game_state.player_in_turn == "1":
             game_state.player_in_turn = "2"
        else:
            game_state.player_in_turn = "1"

        # Make a test move.
        game_state.make_move(col)

        if four_in_a_row(game_state, col, row):
            move_list.append(col)

        # Undo the move.
        game_state.undo_last_move()

        # Undo the null move
        if game_state.player_in_turn == "1":
             game_state.player_in_turn = "2"
        else:
            game_state.player_in_turn = "1"

    return move_list

def computer_move_level_1(game_state):
    x = random.random()
    if x < 0.3:
        return computer_move(game_state, 1, heuristic_function_constant)
    else:
        return computer_move(game_state, 2, heuristic_function_constant)

def computer_move_level_2(game_state):
    x = random.random()
    if x < 0.3:
        return computer_move(game_state, 3, heuristic_function_constant)
    else:
        return computer_move(game_state, 3, heuristic_function_4)

def computer_move_level_3(game_state):
    available_moves = game_state.available_moves()

    # Depth for the minimax algorithm is chosen based
    # on the number of filled columns.
    columns = len(available_moves)
    if columns < 3:
        depth = 20
    if 3 <= columns < 5:
        depth = 10
    else:
        depth = 6
        if game_state.number_of_moves == 0:
            return 3

    return computer_move(game_state, depth, heuristic_function_3)

def negamax(game_state, depth, alpha=-10000, beta=10000):

    global transposition_table

    # If terminal node (win or board full).
    if win_last_move(game_state):
        return -(1000 + depth)
    if game_state.number_of_moves == 42:
        return 0

    # If not terminal node, but depth 0.
    if depth == 0:
        return 0

    # Check if the transposition is in the transposition table.
    if depth > 1:
        key = game_state.key()
        value = transposition_table.get(key)
        if value != None:
            return value

    # Else, return a value based on child node values.

    available_moves = game_state.available_moves()

    # Testing central moves first combined with pruning saves time.
    for move in [3,2,4,1,5,0,6]:
        if move in available_moves:
            game_state.make_move(move)
            new_value = -negamax(game_state, depth-1, -beta, -alpha)
            game_state.undo_last_move()
            alpha = max(alpha, new_value)
            if beta <= alpha:
                break

    if depth > 1:
        transposition_table.update({game_state.key():alpha})
    return alpha

def computer_move(game_state, depth, heuristic_function):
    """Return a move computed by using the minimax algorithm
    and heuristic evaluations.
    """
    def best_moves(move_list, value_list):
        best_value = max(value_list)
        return [move_list[i] for i in range(len(move_list))
                if value_list[i] == best_value]

    # The transposition table is reset.
    global transposition_table
    transposition_table = dict()

    available_moves = game_state.available_moves()

    # The moves are shuffled in order to make the move order
    # more natural for weak heuristic functions.
    random.shuffle(available_moves)

    def search_key(move):
        return heuristic_function(game_state, move)

    # The available moves are sorted based on the heuristic function.
    available_moves.sort(key=search_key, reverse=True)

    alpha = -10000
    beta = 10000
    for move in available_moves:
        game_state.make_move(move)
        new_value = -negamax(game_state, depth, -beta, -alpha)
        game_state.undo_last_move()
        if new_value > alpha:
            best_move = move
            alpha = new_value

    # If there are only losing moves, chose one that is blocking a four in a row
    # if there exist such moves.
    if alpha < 0:
        move_list = blocking_moves(game_state)
        if move_list:
            return heuristic_move(game_state, move_list, heuristic_function)

    return best_move

