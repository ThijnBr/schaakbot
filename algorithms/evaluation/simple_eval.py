def simple_eval(chess):
    """
    Simple evaluation function that calculates material balance.
    Positive values are good for white, negative values are good for black.
    """
    piece_values = {
        'pawn': 1,
        'knight': 3,
        'bishop': 3,
        'rook': 5,
        'queen': 9,
        'king': 0  # King value is not used in evaluation
    }

    total_evaluation = 0

    for y in range(8):
        for x in range(8):
            piece = chess.board[y][x]
            if piece:
                value = piece_values[piece.name]
                if piece.color == 'white':
                    total_evaluation += value
                else:
                    total_evaluation -= value

    return total_evaluation