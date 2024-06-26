from piece.sub_pieces import Pawn

def setup_en_passant(chess, piece, start_y, end_y, end_x):
    """
    Function to setup en passant for next move
    """
    if isinstance(piece, Pawn) and abs(start_y - end_y) == 2:
        chess.en_passant_target = (end_y, end_x)
        return (end_y, end_x)
    else:
        chess.en_passant_target = None
        return None
        
def check_for_en_passant_capture(chess, piece, start_x, end_y, end_x):
    direction = 1 if chess.current_turn == 'white' else -1
    if isinstance(piece, Pawn) and chess.en_passant_target != None:
        # If its a capture, start_x and end_x cant be equalling
        if start_x != end_x:
            target_piece_y, target_piece_x = chess.en_passant_target
            # Check if the capture is a en passant capture. 
            if (end_y + direction == target_piece_y) and end_x == target_piece_x:
                return True
    return False

def en_passant_capture_move(chess, start_y, start_x, end_y, end_x):
    direction = 1 if chess.current_turn == 'white' else -1
    capture_y = end_y + direction
    capture_x = end_x

    chess.board[capture_y, capture_x] = None
    chess.board[end_y, end_x] = Pawn(chess.current_turn)
    chess.board[start_y, start_x] = None

