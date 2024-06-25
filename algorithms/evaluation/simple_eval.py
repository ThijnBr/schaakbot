def simple_eval(chess):
    """
    Simple evaluation function that calculates material balance.
    Positive values are good for white, negative values are good for black.
    """
    total_evaluation = 0

    for y in range(8):
        for x in range(8):
            piece = chess.board[y][x]
            if piece:
                value = piece.value
                if piece.color == 'white':
                    total_evaluation += value
                else:
                    total_evaluation -= value

    return total_evaluation