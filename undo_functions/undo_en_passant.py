from piece.sub_pieces import Pawn

def undo_en_passant(chess, start_y, start_x, end_y, end_x):
    turn = 'white' if chess.current_turn == 'black' else 'black'
    direction = 1 if turn == 'white' else -1

    chess.board[end_y][end_x] = Pawn(turn)
    chess.board[start_y][start_x] = None
    chess.board[start_y + direction][start_x] = Pawn(chess.current_turn)
