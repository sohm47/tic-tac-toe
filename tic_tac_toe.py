from random import randint
from time import time

MAX_VALUE = 1000
MIN_VALUE = -1000

BOARD = [[' ', ' ', ' '], 
         [' ', ' ', ' '], 
         [' ', ' ', ' ']]

SCORE = {'X': -1, '0': 0, 'O': 1}
END_RESULT = {'X': 'AI', '0': 'Human'}

ERROR_MSG = 'Invalid coordinates, try again.'

AI = 'X'
HUMAN = 'O'


def display_board():
    """Displays the current state of the Tic-Tac-Toe board.
    'X' is the AI and 'O' is the Human player.
    """
    print(BOARD[0])
    print(BOARD[1])
    print(BOARD[2])
    print()

    
def check_result():
    """Checks the board for a tie or a winner.
    Returns:
        X if AI wins
        O if Human wins
        0 if it's a tie
        None if there is no winner yet
    """
    winner = None
    
    # Horizontal
    for i in range(3):
        if BOARD[i][0] != ' ' and BOARD[i][0] == BOARD[i][1] \
                              and BOARD[i][0] == BOARD[i][2]:
            winner = BOARD[i][0]
            break
            
    # Vertical
    for i in range(3):
        if BOARD[0][i] != ' ' and BOARD[0][i] == BOARD[1][i] \
                              and BOARD[0][i] == BOARD[2][i]:
            winner = BOARD[0][i]
            break
            
    # Diagonal
    if BOARD[0][0] != ' ' and BOARD[0][0] == BOARD[1][1] \
                          and BOARD[0][0] == BOARD[2][2]:
        winner = BOARD[0][0]
        
    if BOARD[0][2] != ' ' and BOARD[0][2] == BOARD[1][1] \
                          and BOARD[0][2] == BOARD[2][0]:
        winner = BOARD[0][2]
        
    # Check open spots
    open_spots = 0
    for i in range(3):
        for j in range(3):
            if BOARD[i][j] == ' ':
                open_spots += 1
    
    if winner == None and open_spots == 0:
        return '0'
        
    return winner
    
    
def minimax(depth, maximizing_player, alpha, beta):
    """Implements minimax algorithm using alpha beta pruning to find 
    best move for caller. Since this is short game with very little 
    complexity, it checks until the deepest level, which is the end of 
    the game.
    
    Parameters:
        depth (int): 
        maximizing_player (boolean): current player
        alpha (int): best move for maximizing player at the current level
        beta (int): best move for minimizing player at the current level

    Returns:
        (int) 
    """
    global BOARD
    
    winner = check_result()
    if winner != None:
        return SCORE[winner]*depth

    if maximizing_player:
        max_val = MIN_VALUE
        for i in range(3):
            for j in range(3):
                if BOARD[i][j] == ' ':
                    BOARD[i][j] = HUMAN
                    val = minimax(depth-1, False, alpha, beta)
                    BOARD[i][j] = ' '
                    max_val = max(max_val, val)
                    alpha = max(alpha, max_val)
                    if beta <= alpha:
                        break
        return max_val
    else:
        min_val = MAX_VALUE
        for i in range(3):
            for j in range(3):
                if BOARD[i][j] == ' ':
                    BOARD[i][j] = AI
                    val = minimax(depth-1, True, alpha, beta)
                    BOARD[i][j] = ' '
                    min_val = min(min_val, val)
                    beta = min(beta, min_val)
                    if beta <= alpha:
                        break
        return min_val


def player_move():
    """Player moves.
    """
    global BOARD, CURRENT_PLAYER
    
    while True:
        # 0 indexed
        coordinates = input('Human move: ')
        coordinates = coordinates.strip().split()
        try:
            x = int(coordinates[0].strip().split()[0])
            y = int(coordinates[1].strip().split()[0])
            if BOARD[x][y] != ' ':
                print(ERROR_MSG)
                continue
            BOARD[x][y] = HUMAN
            break
        except Exception as e:
            print(ERROR_MSG)
        
    CURRENT_PLAYER = False


def ai_move():
    """AI moves using minimax algorithm.
    """
    global BOARD, CURRENT_PLAYER
    best_score = MAX_VALUE
    move = []
    alpha = MIN_VALUE
    beta = MAX_VALUE
    
    for i in range(3):
        for j in range(3):
            if BOARD[i][j] == ' ':
                BOARD[i][j] = AI
                score = minimax(10, True, alpha, beta)
                BOARD[i][j] = ' '
                
                if score < best_score:
                    best_score = score
                    move = [i,j]
                beta = min(beta, best_score)
    
    print('AI move: {0} {1}'.format(move[0], move[1]))
    BOARD[move[0]][move[1]] = AI
    CURRENT_PLAYER = True


# Deciding who starts the game first
CURRENT_PLAYER = True
random_player = randint(0,1)
if random_player == 1:
    CURRENT_PLAYER = False


# Game
while True:
    result = check_result()
    if result == None:
        if CURRENT_PLAYER:
            player_move()
        else:
            ai_move()
        display_board()
    else:
        if result == '0':
            print('It is a tie')
        else:
            print('Winner is ' + END_RESULT[result])
        break
 
