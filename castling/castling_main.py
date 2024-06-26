from piece.sub_pieces import King, Rook
def check_castling_move(chess, piece, start_x, end_x):
    """
    params:
    (class Piece) piece
    (int) start_x
    (int) end_x

    Function to check if move is a castling move

    Returns:
    bool: True if king else False
    """
    if isinstance(piece, King) and abs(end_x - start_x) == 2 and not chess.is_in_check(chess.current_turn):
        return True
    return False
def castling_move(chess, piece, end_x):
    """
    params:
    (class Board) chess
    (class Piece) piece
    (int) end_x

    Function to check which side to castle. Then perform castling move.

    Returns:
    bool, bool
    """
    is_short_castle, is_long_castle = False, False
    if end_x == 6:
        is_short_castle = True
        perform_castling(True, chess.board, piece.color)
    elif end_x == 2:
        is_long_castle = True
        perform_castling(False, chess.board, piece.color)
    return is_short_castle, is_long_castle

def perform_castling(short_side_castling, board, current_turn):
    """
    params:
    (bool) short_side_castling
    (3D list) board
    (string) current_turn
    """
    # Sets rank based on current_turn color
    y = 7 if current_turn == 'white' else 0
    # Short side castling
    if short_side_castling:
        board[y, 4] = None
        board[y, 7] = None
        board[y, 6] = King(current_turn)
        board[y, 5] = Rook(current_turn)
    # Long side castling
    else:
        board[y, 4] = None
        board[y, 0] = None
        board[y, 2] = King(current_turn)
        board[y, 3] = Rook(current_turn)