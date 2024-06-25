from board.chess_board import Chess
from algorithms.minmax import standard_minimax
import time

def evaluate_board_position(fen, depth, is_maximizing):
    chess = Chess(fen)
    evaluated_move = standard_minimax(chess, depth, is_maximizing)
    return evaluated_move

def iterative_deepening_minimax(fen, is_maximizing, max_time):
    start_time = time.time()
    depth_counter = 1
    best_move = None
    chess = Chess(fen)
    best_eval = float('-inf') if is_maximizing else float('inf')

    while True:
        # Perform minimax with the current depth
        evaluated_move, _ = standard_minimax(chess, depth_counter, is_maximizing)

        # Update best move and evaluation if better move found
        if (is_maximizing and evaluated_move > best_eval) or (not is_maximizing and evaluated_move < best_eval):
            best_eval = evaluated_move
            best_move = _

        # Check elapsed time
        elapsed_time = time.time() - start_time
        
        if elapsed_time >= max_time:
            break
        
        # Increment depth counter for next iteration
        depth_counter += 1

    return best_eval, best_move

def main():
    evaluation = iterative_deepening_minimax('', True, 5)
    print(evaluation)

if __name__ == "__main__":
    main()