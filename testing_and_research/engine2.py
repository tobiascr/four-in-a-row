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
            return game_state.columns[column][row]
        
        def disks_are_of_same_type(col_row_pair_set):
            type_ = None
            all_equal = True      
            for (column, row) in col_row_pair_set:
                if type_ == None:
                    type_ = disk_type(column, row)            
                if type_ == 0:
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
    """Instances of this object stores game states. A game state is stored as
    a list of seven lists of lengths 6. The lists inside the list correspond
    to the columns. Empty positions are stored as 0. The players are called 1 and -1,
    where 1 always make the first move. The first entries in the column lists corresponds to the
    bottom positions. Some extra data are stored here that can be derived from
    the game state, which can help to make some algorithms faster.
    """
    def __init__(self):
        self.columns = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
                          [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.number_of_moves = 0
        self.column_height = [0,0,0,0,0,0,0]
        self.move_sequence = []
        self.player_in_turn = 1
        
    def available_moves(self):
        return [move for move in range(7) if self.column_height[move] < 6]
                 
    def make_move(self, column):
        self.columns[column][self.column_height[column]] = self.player_in_turn
        self.move_sequence.append(column)
        self.column_height[column] += 1
        self.player_in_turn = -self.player_in_turn
        self.number_of_moves += 1
        
    def undo_last_move(self):
        last_move = self.move_sequence[-1]
        self.column_height[last_move] -= 1
        self.columns[last_move][self.column_height[last_move]] = 0
        del self.move_sequence[-1]
        self.player_in_turn = -self.player_in_turn
        self.number_of_moves -= 1
        
def four_in_a_row(game_state, col, row):
    """True iff there is a four in a row that includes the position (col, row)."""
    player = game_state.columns[col][row]

    # Columns. It might be best to try this first, because it's
    # the fastest four in a row to test.
    if row > 2:
        if (player ==
            game_state.columns[col][row-1] ==
            game_state.columns[col][row-2] ==
            game_state.columns[col][row-3]): return True

    # Rows
    in_row = 1
    while col-in_row >= 0:
        if game_state.columns[col-in_row][row] == player:
            in_row += 1
        else:
            break
    n = 1
    while col+n <= 6:
        if game_state.columns[col+n][row] == player:
            in_row += 1
            n += 1
        else:
            break

    if in_row >= 4:
        return True

    # Diagonals
    in_row = 1
    while col-in_row >= 0 and row-in_row >= 0:
        if game_state.columns[col-in_row][row-in_row] == player:
            in_row += 1
        else:
            break
    n = 1
    while col+n <= 6 and row+n <= 5:
        if game_state.columns[col+n][row+n] == player:
            in_row += 1
            n += 1
        else:
            break

    if in_row >= 4:
        return True

    in_row = 1
    while col-in_row >= 0 and row+in_row <= 5:
        if game_state.columns[col-in_row][row+in_row] == player:
            in_row += 1
        else:
            break
    n = 1
    while col+n <= 6 and row-n >= 0:
        if game_state.columns[col+n][row-n] == player:
            in_row += 1
            n += 1
        else:
            break
    
    if in_row >= 4:
        return True

    return False
    
def win_last_move(game_state):
    """True iff the last move made gives four in a row."""
    col = game_state.move_sequence[-1]
    row = game_state.column_height[col] - 1
    return four_in_a_row(game_state, col, row)
     
def minimax_value(game_state, depth, pruning):
    """Maximizes if the player in the last move is 1 and minimizes if -1.
    pruning is True or False.
    """        
    # If terminal node (win or board full).
    if win_last_move(game_state):
        return -(1000 + depth) * game_state.player_in_turn
    if game_state.number_of_moves == 42:
        return 0

    # If not terminal node, but depth 0.
    if depth == 0:
        return 0

    # Else, return a value based on child node values.
    values = []
    available_moves = game_state.available_moves()

    # Testing central moves first combined with pruning saves time.
    for move in [3,2,4,1,5,0,6]:
        if move in available_moves:
            game_state.make_move(move)
            value = minimax_value(game_state, depth-1, pruning)
            values.append(value)
            game_state.undo_last_move()
            
            if pruning:
                if game_state.player_in_turn == 1:
                    if value > 0: break
                else:
                    if value < 0: break            
            
    # If maximizing player made the last move.
    if game_state.player_in_turn == -1:
        return min(values)

    # If minimizing player made the last move.
    else:
        return max(values)       
    
def heuristic_function_constant(game_state, move):
    return 0

def heuristic_function_1(game_state, move):
    """Give a heuristic evaluation in form of a number
    of how good it would be to make "move" to "game_state". The value is
    higher the better the move, regardless of the player to make it.
    
    This function give higher values to more central columns.
    """
    return -abs(3 - move)
    
def heuristic_function_2(game_state, move):
    """Give a heuristic evaluation in form of a number
    of how good it would be to make "move" to "game_state". The value is
    higher the better the move, regardless of the player to make it.
    
    This function counts possible four in a rows further into the game.
    Test shows that this function is weak compared to favouring central moves.
    """    
    game_state.make_move(move)
    value = -game_state.player_in_turn 
    number_of_possible_four_in_a_rows = 0
        
    for col in range(7):
        for row in range(game_state.column_height[col], 6):
            # Make a test move
            game_state.columns[col][row] = value
            if four_in_a_row(game_state, col, row):
                number_of_possible_four_in_a_rows += 1
            # Undo the move
            game_state.columns[col][row] = 0
                
    game_state.undo_last_move()

    return number_of_possible_four_in_a_rows

def heuristic_function_3(game_state, move):
    """Give a heuristic evaluation in form of a number
    of how good it would be to make "move" to "game_state". The value is
    higher the better the move, regardless of the player to make it.
    
    This function give higher values to more central columns and rows.
    Test shows that this function is stronger than the above heuristic functions.
    """
    row = game_state.column_height[move]
    return -abs(3 - move) - abs(2.5 - row)

def evaluate_move_minimax(game_state, depth, move, pruning):
    game_state.make_move(move)
    value = minimax_value(game_state, depth, pruning)
    game_state.undo_last_move()            
    return value

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

def blocking_move(game_state):
    """Return a move that blocks an immediate four in a row for the opponent if
    such move exist. Else return None.
    """
    available_moves = game_state.available_moves() 
    for col in [3,2,4,1,5,0,6]:
        if col in available_moves:
            row = game_state.column_height[col]
            # Make a test move.
            game_state.columns[col][row] = -game_state.player_in_turn
            
            if four_in_a_row(game_state, col, row):
                return col
            
            # Undo the move.
            game_state.columns[col][row] = 0
            
def computer_move_level_1(game_state):
    x = random.random()
    if x < 0.3:        
        return computer_move(game_state, 0, heuristic_function_constant)
    else:
        return computer_move(game_state, 1, heuristic_function_constant)

def computer_move_level_2(game_state):
    return computer_move(game_state, 4, heuristic_function_constant)
    
def computer_move_level_3(game_state):
    available_moves = game_state.available_moves()
    
    # Depth for the minimax algorithm is chosen based
    # on the number of filled columns.
    if len(available_moves) < 3:
        depth = 12
    if 3 <= len (available_moves) < 5:
        depth = 6
    if 5 <= len(available_moves):
        depth = 4
        
    return computer_move(game_state, depth, heuristic_function_3)
        
def computer_move(game_state, depth, heuristic_function):
    """Return a move computed by using the minimax algorithm
    and heuristic evaluations.
    """
    available_moves = game_state.available_moves()
    pruning = True  
    minimax_values = [evaluate_move_minimax(game_state, depth, i, pruning)
                      for i in available_moves]
    
    # If maximizing player.
    if game_state.player_in_turn == 1:
        best_value = max(minimax_values)
    # If minimizing player.
    else:
        best_value = min(minimax_values)
    best_move = available_moves[minimax_values.index(best_value)]

    # If 0 is the best rating, then make a heuristic choice among the 0-rated moves.
    if best_value == 0:        
        neutral_moves = [available_moves[i] for i in range(len(available_moves))
                         if minimax_values[i] == 0]
        best_move = heuristic_move(game_state, neutral_moves, heuristic_function)                       

    # If there are only losing moves, chose one that is blocking a four in a row
    # if there exist such moves.
    if ((game_state.player_in_turn == 1 and best_value < 0) or
       (game_state.player_in_turn == -1 and best_value > 0)):
            move = blocking_move(game_state)
            if move != None:
                best_move = move
    return best_move
        
