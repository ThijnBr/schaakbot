from algorithms.evaluation.piece_square_evaluation import evaluate_piece_square
from algorithms.evaluation.simple_eval import simple_eval
from piece.sub_pieces import Rook, Bishop, Queen, Knight, Pawn, King
from undo_functions.undo_main import undo_move

available_promotion_piece = [Rook, Bishop, Queen, Knight]

def evaluate_board(chess):
    """
    Function to evaluate the current board state based on different factors.
    """
    total_eval = 0

    white_piece_positions, black_piece_positions = get_piece_positions(chess)

    # Evaluate based on piece-square tables
    total_eval += evaluate_piece_square(chess) / 10

    # Evaluate material balance
    total_eval += simple_eval(chess) * 10

    # Evaluate control of the center
    total_eval += evaluate_control_of_center(chess) * 10

    # Evaluate development
    total_eval += evaluate_piece_development(white_piece_positions, black_piece_positions) * 5

    # Evaluate king safety
    total_eval += evaluate_king_safety(chess) * 10

    return total_eval

def get_piece_positions(chess):
    white_positions = []
    black_positions = []
    for y in range(8):
        for x in range(8):
            piece = chess.board[y, x]
            if piece:
                if piece.color == 'white':
                    white_positions.append((y, x))
                else:
                    black_positions.append((y, x))
    return white_positions, black_positions

def evaluate_control_of_center(chess):
    """
    Evaluates control over central squares.
    """
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    white_control = sum(1 for sq in center_squares if chess.board[sq[0], sq[1]] and chess.board[sq[0], sq[1]].color == 'white')
    black_control = sum(1 for sq in center_squares if chess.board[sq[0], sq[1]] and chess.board[sq[0], sq[1]].color == 'black')
    return white_control - black_control

def evaluate_piece_development(white_pieces_positions, black_pieces_positions):
    """
    Evaluates piece development.
    """
    white_development = sum(1 for pos in white_pieces_positions if pos[0] >= 4)
    black_development = sum(1 for pos in black_pieces_positions if pos[0] <= 3)
    return white_development - black_development

def evaluate_king_safety(chess):
    """
    Evaluates the safety of the kings.
    """
    white_king_position = chess.find_king_position('white')
    black_king_position = chess.find_king_position('black')

    white_king_safety = evaluate_king_position(chess, white_king_position)
    black_king_safety = evaluate_king_position(chess, black_king_position)

    return white_king_safety - black_king_safety

def evaluate_king_position(chess, king_position):
    """
    Helper function to evaluate the safety of a king's position.
    """
    if not king_position:
        return 0  # No king found, return neutral score

    y, x = king_position
    king_safety_score = 0

    # Check for pieces around the king
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            ny, nx = y + dy, x + dx
            if chess.is_in_bounds(ny, nx):
                piece = chess.board[ny, nx]
                if piece:
                    if piece.color == 'white':
                        king_safety_score += 1
                    else:
                        king_safety_score -= 1

    return king_safety_score
