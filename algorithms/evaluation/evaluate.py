from algorithms.evaluation.piece_square_evaluation import evaluate_piece_square

def evaluate_board(chess):
    total_eval = 0
    total_eval += evaluate_piece_square(chess)
    return total_eval

