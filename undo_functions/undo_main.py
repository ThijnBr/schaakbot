from piece.sub_pieces import King, Rook
from undo_functions.undo_castling import undo_castling, undo_castling_state
def undo_move(chess):
        """
        params:
        (class Chess) chess

        Function to undo a move. 

        Returns:
        bool: returns false if no history, returns true if undo move is done
        """
        if not chess.history:
            return False
        
        historical_move = chess.history.pop()
        start, end, target_piece, is_short_castle, is_long_castle, first_king_move, is_first_rook_move = historical_move

        # Initialize start and end positions as y and x coordinates
        start_y, start_x = start
        end_y, end_x = end
        
        
        # If its not a castling move, undo standard move.
        if not undo_castling_move(chess, is_short_castle, is_long_castle):
            chess.board[start_y][start_x] = chess.board[end_y][end_x]
            chess.board[end_y][end_x] = target_piece

        # Undo castling state in Chess instance
        undo_castling_state(chess, start, first_king_move, is_first_rook_move)

        # Switch turn
        chess.switch_turn()
        return True

def undo_castling_move(chess, is_short_castle, is_long_castle):
    """
    params:
    (class Chess) chess
    (bool) is_short_castle
    (bool) is_long_castle

    Function to undo a castling move completly.

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