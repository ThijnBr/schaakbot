from algorithms.evaluation.evaluate import evaluate_board
from undo_functions.undo_main import undo_move
from piece.sub_pieces import Rook, Bishop, Queen, Knight, Pawn

available_promotion_piece = [Rook, Bishop, Queen, Knight]

def standard_minimax(chess, depth, maximizing_player, alpha=-float(1_000_000), beta=float(1_000_000)):
    """
    params:
    (class Board) chess
    (int) depth
    (float) alpha
    (float) beta

    Function to determine best move on the board using the minimax algorithm.

    Returns:
    (float) evaluated position, (tuple) -> old_pos to new_pos
    """
    current_turn = chess.current_turn

    if chess.is_checkmate(current_turn):
        return float(1_000_000) if current_turn == 'white' else -float(1_000_000), None
    
    if chess.is_draw(current_turn):
        return 0, None

    if depth == 0:
        return evaluate_board(chess), None  # return evaluation score and best move

    
    promotion_rank = 0 if current_turn == 'white' else 7

    best_eval = -float(1_000_000) if maximizing_player else float(1_000_000)
    best_move = None

    for y in range(8):
        for x in range(8):
            # Get piece on board
            piece = chess.board[y, x]
            if piece and piece.color == current_turn:
                # Get possible moves of piece on board
                piece_moves = piece.get_possible_moves((y, x), chess)
                for new_pos in piece_moves:
                    old_pos = (y, x)
                    is_pawn_promotion = isinstance(piece, Pawn) and new_pos[0] == promotion_rank

                    # Handle pawn promotion
                    if is_pawn_promotion:
                        for promotion_piece in available_promotion_piece:
                            # Make a promotion for every possible piece.
                            chess.make_move(old_pos, new_pos, promotion_piece(current_turn))
                            evaluation, _ = standard_minimax(chess, depth - 1, not maximizing_player, alpha, beta)
                            if maximizing_player:
                                if evaluation > best_eval:
                                    best_eval = evaluation
                                    best_move = (old_pos, new_pos, promotion_piece)
                                alpha = max(alpha, best_eval)
                            else:
                                if evaluation < best_eval:
                                    best_eval = evaluation
                                    best_move = (old_pos, new_pos, promotion_piece)
                                beta = min(beta, best_eval)
                            undo_move(chess)
                            if beta <= alpha:
                                break
                    else:
                        chess.make_move(old_pos, new_pos)      
                        
                        evaluation, _ = standard_minimax(chess, depth - 1, not maximizing_player, alpha, beta)
                        if maximizing_player:
                            if evaluation > best_eval:
                                best_eval = evaluation
                                best_move = (old_pos, new_pos)
                            alpha = max(alpha, best_eval)
                        else:
                            if evaluation < best_eval:
                                best_eval = evaluation
                                best_move = (old_pos, new_pos)
                            beta = min(beta, best_eval)
                        undo_move(chess)
                        if beta <= alpha:
                            break

    return best_eval, best_move
