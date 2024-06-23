from piece.sub_pieces import King, Rook
def check_for_king_movement(chess, piece, first_king_move) -> bool:
    """
    params:
    (class Board) chess
    (class Piece) piece
    (bool) first_king_move

    Function to check if it's the first king_move made. 
    
    Returns: 
    bool: original value False, or True if its the first king move.
    """
    # Check if piece is King
    if isinstance(piece, King):
        # Check if turn is white and check if white king has moved.
        if chess.current_turn == 'white' and not chess.white_king_moved:
            first_king_move = True
            chess.castle_short_white = False
            chess.castle_long_white = False
        # Check if turn is black and check if black king has moved
        if chess.current_turn == 'black' and not chess.black_king_moved:
            first_king_move = True
            chess.castle_short_black = False
            chess.castle_long_black = False
    return first_king_move
    
def check_for_rook_movement(chess, piece, start, is_first_rook_move) -> bool:
    """
    params:
    (class Chess) chess
    (class Piece) piece
    (Tuple (y, x)) start
    (bool) is_first_rook_move

    Function to check if it's the first rook move for a specific rook in the corner of the board. 
    Returns:
    bool: original value False if not first rook move. Else return True
    """
    # Start should be one of the corners of the board.
    def handle_white_rook_movement():
        nonlocal is_first_rook_move
        if start == (7, 0) and chess.castle_long_white:
            is_first_rook_move = True
            chess.white_rook_long_moved = True
            chess.castle_long_white = False
        elif start == (7, 7) and chess.castle_short_white:
            is_first_rook_move = True
            chess.white_rook_short_moved = True
            chess.castle_short_white = False
    
    def handle_black_rook_movement():
        nonlocal is_first_rook_move
        if start == (0, 0) and chess.castle_long_black:
            is_first_rook_move = True
            chess.black_rook_long_moved = True
            chess.castle_long_black = False
        elif start == (0, 7) and chess.castle_short_black:
            is_first_rook_move = True
            chess.black_rook_short_moved = True
            chess.castle_short_black = False

    # Check if piece is Rook
    if isinstance(piece, Rook):
        if chess.current_turn == 'white':
            handle_white_rook_movement()
        elif chess.current_turn == 'black':
            handle_black_rook_movement()

    return is_first_rook_move
