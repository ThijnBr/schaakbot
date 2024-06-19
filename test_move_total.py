from chessStructure import Chess

def perft(chess, depth):
    if depth == 0:
        return 1

    total_moves = 0
    for y, row in enumerate(chess.board):
        for x, piece in enumerate(row):
            if piece != '. ' and piece[0] == 'w':
                piece_moves = chess.check_moveable_positions(piece, (x, y))
                for new_pos in piece_moves:
                    old_pos = (x, y)
                    undoboard = chess.copy()
                    chess.move_piece(piece, old_pos, new_pos)
                    total_moves += perft(chess, depth - 1)
                    chess = undoboard

    return total_moves

def main():
    chess = Chess()
    chess.initialize_pieces()
    total_moves = perft(chess, 2)
    print("Total moves: ", total_moves)

if __name__ == "__main__":
    main()
