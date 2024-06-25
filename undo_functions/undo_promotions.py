from piece.sub_pieces import Pawn

def undo_promotion(chess, start_y, start_x, end_y, end_x, captured_piece):
    turn = 'white' if chess.current_turn == 'black' else 'black'
    chess.board[end_y][end_x] = captured_piece
    chess.board[start_y][start_x] = Pawn(turn)
