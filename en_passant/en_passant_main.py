from piece.sub_pieces import Pawn
def check_en_passant_possible(chess, piece, start_y, end_y, end_x) -> tuple:
    """
    params:
    (class Piece) piece
    (int) start_y
    (int) end_y

    Function to check if en_passant is possible for opponent in next move.

    Returns:
    (tuple (y, x)) position
    """
    if isinstance(piece, Pawn):
        # Check if the pawn move was a two-square move
        if abs(end_y - start_y) == 2:
            # Set the en_passant_target
            chess.en_passant_target = (end_y, end_x)
            return chess.en_passant_target

def check_for_en_passant_capture(chess, piece, end_y, end_x, color):
    """
    params:
    (class Chess) chess
    (int) end_y
    (int) end_x
    (string) color
    """
    # Set direction based on current turn
    direction = 1 if color == 'white' else -1

    # Check if there is a target
    if chess.en_passant_target and isinstance(piece, Pawn):
        en_passant_piece_y, en_capture_x = chess.en_passant_target

        # capture_y is one square below the target pawn
        capture_y = en_passant_piece_y - direction

        # if the end position is equal to the capture square return true
        if (capture_y, en_capture_x) == (end_y, end_x):
             return True
    return False

def en_passant_capture_move(chess, start_y, start_x):
    """
    params:
    (class Chess) chess
    (int) start_y
    (int) start_x

    Function to do a en passant capture
    """
    capture_y, capture_x = chess.en_passant_target

    # Set direction based on turn
    direction = 1 if chess.current_turn == 'white' else -1
    end_y = capture_y - direction
    chess.board[end_y][capture_x] = Pawn(chess.current_turn)
    chess.board[capture_y][capture_x] = None
    chess.board[start_y][start_x] = None
