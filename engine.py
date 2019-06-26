import random
from multiprocessing import Pool

class EngineInterface():
    """This class and the GameState class is intended to be the interface for this module.
    """    
    def __init__(self, difficulty_level):
        """difficulty_level can be 1, 2 or 3.
        """
        self.difficulty_level = difficulty_level

    def engine_move(self, game_state):
        if self.difficulty_level == 1:
            return random_move(game_state)
        if self.difficulty_level == 2:            
            if game_state.number_of_moves <= 1:
                return random_move(game_state)
            depth = 2
            values = [evaluate_move_minimax([game_state, depth, i]) for i in game_state.available_moves()]
            
            # Now find the best move based on the above computations.
            neutral_moves = []
            best_value = -10000 * game_state.player_in_turn
            for i in range(len(available_moves)):
                if result[i] == 0:
                    neutral_moves.append(available_moves[i])
                # If maximizing player.
                if game_state.player_in_turn == 1:
                    if result[i] > best_value:
                        best_value = result[i]
                        best_move = available_moves[i]
                # If minimizing player.
                else:
                    if result[i] < best_value:
                        best_value = result[i]
                        best_move = available_moves[i]
                        
            # If 0 is the best rating, then make a heuristic choise among the 0-rated moves.
            if best_value == 0:
               best_value = -10000
               for move in neutral_moves:
                   value = heuristic_value_1(game_state, move)
                   if value > best_value:
                       best_value = value
                       best_move = move            
                
        if self.difficulty_level == 3:
            return computer_move(game_state)
        
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
        
    def four_in_a_row_positions():
        """Return a list of (row, column) pairs for the positions that gives one
        or several four rows. It is assumed that the player that made the last move
        made a winning move. The list of positions is useful for highlighting
        the disks that made a four in a row in a GUI.
        """
        pass        

    
def win_last_move(game_state):
    """True iff the last move made gives 4 in a row."""
    col = game_state.move_sequence[-1]
    player_in_last_move = -game_state.player_in_turn
        
    # Row (0-5) where the disk in the move is placed.
    row = game_state.column_height[col] - 1

    # Columns. It might be best to try this first, because it's
    # the fastest four in a row to test.
    if row > 2:
        if (player_in_last_move ==
            game_state.columns[col][row-1] ==
            game_state.columns[col][row-2] ==
            game_state.columns[col][row-3]): return True

    # Rows
    in_row = 1
    while col-in_row >= 0:
        if game_state.columns[col-in_row][row] == player_in_last_move:
            in_row += 1
        else:
            break
    n = 1
    while col+n <= 6:
        if game_state.columns[col+n][row] == player_in_last_move:
            in_row += 1
            n += 1
        else:
            break

    if in_row >= 4:
        return True

    # Diagonals
    in_row = 1
    while col-in_row >= 0 and row-in_row >= 0:
        if game_state.columns[col-in_row][row-in_row] == player_in_last_move:
            in_row += 1
        else:
            break
    n = 1
    while col+n <= 6 and row+n <= 5:
        if game_state.columns[col+n][row+n] == player_in_last_move:
            in_row += 1
            n += 1
        else:
            break

    if in_row >= 4:
        return True

    in_row = 1
    while col-in_row >= 0 and row+in_row <= 5:
        if game_state.columns[col-in_row][row+in_row] == player_in_last_move:
            in_row += 1
        else:
            break
    n = 1
    while col+n <= 6 and row-n >= 0:
        if game_state.columns[col+n][row-n] == player_in_last_move:
            in_row += 1
            n += 1
        else:
            break
    
    if in_row >= 4:
        return True

    return False

def random_move(game_state):
    """Return a randomly chosen move (0-6)."""
    available_moves = game_state.available_moves()
    
    return available_moves[random.randrange(len(available_moves))]
     
def minimax_value(game_state, depth):
    """Maximizes if the player in the last move is 1 and minimizes if -1."""        
    # If terminal node (win or board full).
    if win_last_move(game_state):
        value = -(1000 + depth) * game_state.player_in_turn
    elif game_state.number_of_moves == 42:
        value = 0

    # If not terminal node, but depth 0, do a heuristic evaluation.
    elif depth == 0:
        value = 0

    # Else, return a value based on child node values.
    
    # If maximizing player made the last move.
    elif game_state.player_in_turn == -1:
        values = []
        available_moves = game_state.available_moves()

        # Testing central moves first combined with pruning saves time.
        test_order = [3,2,4,1,5,0,6]
        for move in test_order:
            if move in available_moves:
                game_state.make_move(move)
                value = minimax_value(game_state, depth-1)
                values.append(value)
                game_state.undo_last_move()

                # Pruning
                if value <= -1000: break
            
        value = min(values)

    # If minimizing player made the last move.
    else:
        values = []
        available_moves = game_state.available_moves()
        
        # Testing central moves first combined with pruning saves time.
        test_order = [3,2,4,1,5,0,6]
        for move in test_order:
            if move in available_moves:
                game_state.make_move(move)
                value = minimax_value(game_state, depth-1)
                values.append(value)
                game_state.undo_last_move()
        
                # Pruning
                if value >= 1000: break
            
        value = max(values)

    return value

def heuristic_value_random(game_state, move):
    return random.random()

def heuristic_value_1(game_state, move):
    """Give a heuristic evaluation in form of a non-negative number
    of how good it would be to make "move" to "game_state". The value is
    higher the better the move, regardless of the player to make it.
    """
    return 10 - abs(3 - move)

def evaluate_move_minimax(arg_list):
    """arg_list = [game_state, depth, move]"""    
    game_state = arg_list[0]
    depth = arg_list[1]
    move = arg_list[2]
        
    game_state.make_move(move)
    value = minimax_value(game_state, depth)
    game_state.undo_last_move()
    
    return value

def computer_move(game_state):
    """Return a move computed by using the minimax algorithm
    and heuristic evaluations.
    """
    available_moves = game_state.available_moves()
    
    # Depth for the minimax algorithm is chosen based
    # on the number of filled columns.
    if len(available_moves) < 3:
        depth = 12
    if 3 <= len (available_moves) < 5:
        depth = 6
    if 5 <= len(available_moves):
        depth = 4
   
    # Parallel computing is used for evaluating moves.
    #p = Pool()
    #result = p.map(evaluate_move_minimax,
    #               [[game_state, depth, i] for i in available_moves])
    #p.close()
    result = [evaluate_move_minimax([game_state, depth, i]) for i in available_moves]

    # Now find the best move based on the above computations.
    neutral_moves = []
    best_value = -10000 * game_state.player_in_turn
    for i in range(len(available_moves)):
        if result[i] == 0:
            neutral_moves.append(available_moves[i])
        # If maximizing player.
        if game_state.player_in_turn == 1:
            if result[i] > best_value:
                best_value = result[i]
                best_move = available_moves[i]
        # If minimizing player.
        else:
            if result[i] < best_value:
                best_value = result[i]
                best_move = available_moves[i]
                
    # If 0 is the best rating, then make a heuristic choise among the 0-rated moves.
    if best_value == 0:
       best_value = -10000
       for move in neutral_moves:
           value = heuristic_value_1(game_state, move)
           if value > best_value:
               best_value = value
               best_move = move     
                              
    return best_move
