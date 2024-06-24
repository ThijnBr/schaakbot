from piece.sub_pieces import King, Rook
def undo_castling_move(chess, is_short_castle, is_long_castle):
    """
    params:
    (class Chess) chess
    (bool) is_short_castle
    (bool) is_long_castle

    Function to undo a castling move completly. This one gets called in undo_move in undo_main.py

    Returns:
    bool: True if move is castling move, false if not.
    """
    # Undo short castle
    if is_short_castle:
        undo_castling(True, chess.board, chess.current_turn)
        return True
    # Undo long castle
    elif is_long_castle:
        undo_castling(False, chess.board, chess.current_turn)
        return True
    return False

def undo_castling(short_side_castle, board, current_turn):
        """
        params:
        (bool) short_side
        (board) 3D list
        (string) current_turn

        Function to undo castling on the board. Only reverts the pieces and not the board state
        """
        # Sets castling rank based on turn
        y = 7 if current_turn != 'white' else 0
        # Sets pieces opposite color of current_turn on board
        color = 'white' if current_turn == 'black' else 'black'
        if short_side_castle:
            board[y][6] = None
            board[y][5] = None
            board[y][4] = King(color)
            board[y][7] = Rook(color)
        else:
            board[y][2] = None
            board[y][3] = None
            board[y][4] = King(color)
            board[y][0] = Rook(color)
    
def undo_castling_state(chess, start, first_king_move, is_first_rook_move):
    """
    params:
    (class Board) chess
    (tuple (y, x)) start
    (bool) first_king_move
    (bool) is_first_rook_move

    Function to undo castling state in class Chess chess. 
    """
    set_king_moved(chess, first_king_move)
    set_rook_moved(chess, start, is_first_rook_move)
    set_castling_state(chess)

def set_king_moved(chess, first_king_move):
    """
    params:
    (class Board) chess
    (bool) first_king_move

    Function to undo white_ or black_ king_moved
    """
    # Check if first king move and set king_moved variables
    if first_king_move:
        if chess.current_turn == 'black':
            chess.white_king_moved = False
        else:
            chess.black_king_moved = False

def set_rook_moved(chess, start, is_first_rook_move):
    """
    params:
    (class Board) chess
    (tuple (y, x)) start
    (bool) is_first_rook_move

    Function to undo (color)_rook_(short/long)_moved
    """
    # Check if first rook move and set rook_moved variables
    if is_first_rook_move:
        if chess.current_turn == 'black':
            if start == (7, 0):
                chess.white_rook_long_moved = False
            elif start == (7, 7):
                chess.white_rook_short_moved = False
        else:
            if start == (0, 0):
                chess.black_rook_long_moved = False
            elif start == (0, 7):
                chess.black_rook_short_moved = False

def set_castling_state(chess):
    """
    params:
    (class Board) chess

    Function to undo castling state. 
    """
    if chess.current_turn == 'black':
        if not chess.white_king_moved:
            if not chess.white_rook_short_moved:
                chess.castle_short_white = True
            if not chess.white_rook_long_moved:
                chess.castle_long_white = True
    else:
        if not chess.black_king_moved:
            if not chess.black_rook_short_moved:
                chess.castle_short_black = True
            if not chess.black_rook_long_moved:
                chess.castle_long_black = True