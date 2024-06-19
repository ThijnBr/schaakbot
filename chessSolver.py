def center_pawns(x, y, color):
    center_positions = {(3, 3), (3, 4), (4, 3), (4, 4)}

    # Extra points for pawns in the center
    if (x, y) in center_positions:
        return 0.5 if color == 'w' else -0.5
    
    return 0

#simple function for evaluation
def evaluate(board, points):
    total = 0
    for y, row in enumerate(board):
        for x, pos in enumerate(row):
            if pos != '. ':
                piece_type = pos[1]
                color = pos[0]
                piece_value = points.get(piece_type, 0)

                # Base points for the piece
                if color == 'w':
                    total += piece_value
                else:
                    total -= piece_value

                # Extra points for pawns
                if piece_type == 'P':
                    total += center_pawns(x, y, color)
                    
    return total

def minimax(Chess, depth, maximizing_player):
    chess = Chess.copy()
    if depth == 0:
        return evaluate(chess.board, chess.points), None
    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for y, row in enumerate(chess.board):
            for x, piece in enumerate(row):
                if piece != '. ' and piece[0] == 'w':
                    piece_moves = chess.check_moveable_positions(piece, (x, y))
                    for new_pos in piece_moves:
                        new_piece = chess.board[y][x]
                        old_pos = (x, y)
                        undoboard = chess.copy()
                        chess.move_piece(new_piece, old_pos, new_pos)
                        evaluation, _= minimax(chess, depth - 1, False)
                        chess = undoboard
                        if evaluation > max_eval:
                            max_eval = evaluation
                            best_move = (new_piece, old_pos, new_pos)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for y, row in enumerate(chess.board):
            for x, piece in enumerate(row):
                if piece != '. ' and piece[0] == 'b':
                    piece_moves = chess.check_moveable_positions(piece, (x, y))
                    for new_pos in piece_moves:
                        new_piece = chess.board[y][x]
                        old_pos = (x, y)
                        undoboard = chess.copy()
                        chess.move_piece(new_piece, old_pos, new_pos)
                        evaluation, _= minimax(chess, depth - 1, True)
                        chess = undoboard
                        if evaluation < min_eval:
                            min_eval = evaluation
                            best_move = (new_piece, old_pos, new_pos)
        return min_eval, best_move
