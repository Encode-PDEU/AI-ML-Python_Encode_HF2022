"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # if count of X on board is equal to count of O on board, then its X's turn, else its O's turn.
    X_count = 0
    O_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                X_count += 1
            if board[i][j] == O:
                O_count += 1

    if X_count == O_count:
        return X
    else:
        return O

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    action = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.add((i,j))

    return action

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # action here is a set of i, j
    i, j = action

    # if action is valid then we will return a board state after impling the action, else will raise an error
    if i <= 2 and j <= 2 and board[i][j] == EMPTY:
        new_board = copy.deepcopy(board)
        new_board[i][j] = player(board)
        return new_board
    
    else:
        raise Exception("Action is Invalid")

    # raise NotImplementedError


def is_over(board):
    # for horizontals and vertical
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X or board[i][0] == O:
                return True

        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X or board[0][i] == O:
                return True

    # for diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        if board[1][1] == X or board[1][1] == O:
            return True

    if board[0][2] == board[1][1] == board[2][0]:
        if board[1][1] == X or board[1][1] == O:
            return True

    return False

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # if someone won and it shows next move (hypothetical) to be of X, that implies O wins and vice versa
    if is_over(board):
        if player(board) == X:
            return O
        else:
            return X    

    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if someone one the game, it's a terminal board
    if is_over(board):
        return True
    
    # if no one wins, and there are empty space that implies more moves to be played
    # therfore it is not terminal board
    # if no cell is empty and no one won, i.e. it's tie then also it's terminal board
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
        return True

    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # if someone has won the game, utility will be 1 or -1 according to who won 
    # X wins --> utility = 1
    # O wins --> utility = -1
    if is_over(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
    
    # if no one won and its a terminal board i.e. it is a tie, then utility will be 0
    if is_over(board) == False and terminal(board) == True:
        return 0

    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if it is already a terminal board, nothing will be returned
    if terminal(board):
        return None

    else:
        # if next move (of AI) is from X, then max_value function is called, and it returns the optimized move
        if player(board) == X:
            value, move = max_value(board)
            return move 
        
        # if next move (of AI) is from O, then min_value function is called, and it returns the optimized move
        else:
            value, move = min_value(board)
            return move

    # raise NotImplementedError

def max_value(board):
    # if it is already a terminal board, it returns the utility of the board
    if terminal(board):
        return utility(board), None
    
    # for getting max value, setting value to -200
    v = -200
    move = None

    # iteration to all possible actions
    for action in actions(board):

        # getting the most optimized utility and move after opponents move
        a, b = min_value(result(board, action))

        # if value is less then utility, change value to that and move to the action through which this is got
        if a > v:
            v = a
            move = action

            # if the value gets to 1 return the move
            if v == 1:
                return v, move

    return v, move

def min_value(board):
    # if it is already a terminal board, it returns the utility of the board
    if terminal(board):
        return utility(board), None
    
    # for getting min value, setting value to 200
    v = 200
    move = None

    # iteration to all possible actions
    for action in actions(board):

        # getting the most optimized utility and move after opponents move
        a, b = max_value(result(board, action))

        # if value is greater then utility, change value to that and move to the action through which this is got
        if a < v:
            v = a
            move = action

            # if the value gets to -1 return the move
            if v == -1:
                return v, move
                
    return v, move