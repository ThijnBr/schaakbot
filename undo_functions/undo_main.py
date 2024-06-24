from piece.sub_pieces import King, Rook
from undo_functions.undo_castling import undo_castling_state, undo_castling_move
from undo_functions.undo_en_passant import undo_en_passant

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
        start, end, target_piece, is_short_castle, is_long_castle, first_king_move, is_first_rook_move, _, en_passant_capture = historical_move

        # Initialize start and end positions as y and x coordinates
        start_y, start_x = start
        end_y, end_x = end
        
        if en_passant_capture:
            undo_en_passant(chess, end_y, end_x, start_y, start_x)
        # If is not a castling move, do a undo default move.
        elif not undo_castling_move(chess, is_short_castle, is_long_castle):
            chess.board[start_y][start_x] = chess.board[end_y][end_x]
            chess.board[end_y][end_x] = target_piece

        if chess.history:
            chess.en_passant_target = chess.history[-1][-2]

        # Undo castling state in Chess instance
        undo_castling_state(chess, start, first_king_move, is_first_rook_move)

        # Switch turn
        chess.switch_turn()
        return True