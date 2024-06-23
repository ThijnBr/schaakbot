from piece.sub_pieces import Pawn
def undo_en_passant_move(chess, end_y, end_x, start_y, start_x):
    color = 'white' if chess.current_turn == 'black' else 'black'
    direction = 1 if color == 'white' else -1

    chess.board[end_y][end_x] = None
    chess.board[start_y][start_x] = Pawn(color)

    opponent_piece_y = end_y + direction
    chess.board[opponent_piece_y][end_x] = Pawn(chess.current_turn)
    