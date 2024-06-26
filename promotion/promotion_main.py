from piece.sub_pieces import Pawn, Queen

def check_for_promotion(piece, end_y):
    """
    params:
    (class Piece) piece
    (int) end_y

    Function to check if promotion is possible.

    Returns:
    bool: True if piece is at end of board. If not, return False
    """
    if piece:
        board_end_y = 0 if piece.color == 'white' else 7
    if isinstance(piece, Pawn) and end_y == board_end_y:
        return True
    return False

def promote_piece(chess, end_y, end_x, promotion_piece):
    """
    params:
    (class Chess) chess
    (int) end_y
    (int) end_x

    Function to promote a piece on the board
    """
    if not promotion_piece:
        promotion_piece = Queen(chess.current_turn)
    chess.board[end_y, end_x] = promotion_piece