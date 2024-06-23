from piece.sub_pieces import Pawn, Rook, Knight, Bishop, Queen, King
def load_from_fen_pieces(chess, fen):
    """
    params:
    (class Board) chess
    (string) fen

    Function to load pieces from a chess fen-string
    """
    piece_map = {
        'p': Pawn, 'r': Rook, 'n': Knight, 'b': Bishop, 'q': Queen, 'k': King
    }
    rows = fen.split('/')
    for i, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                col += int(char)
            else:
                color = 'white' if char.isupper() else 'black'
                piece_type = piece_map[char.lower()]
                chess.board[i][col] = piece_type(color)
                col += 1
    
def load_from_fen_castle(chess, fen):
    """
    params:
    (class Board) chess
    (string) fen

    Function to load castling state from fen
    """
    for char in fen:
        match char:
            case '-':
                return
            case 'K':
                chess.castle_short_white = True
            case 'Q':
                chess.castle_long_white = True
            case 'k':
                chess.castle_short_black = True
            case 'q':
                chess.castle_long_black = True

def load_from_fen_player_to_move(chess, fen):
    """
    params:
    (class Board) chess
    (string) fen

    Function to load player to move from fen
    """
    chess.current_turn = 'black' if fen == 'b' else 'white'

def load_from_fen(chess, fen):
    """
    params:
    (class Board) chess
    (string) fen

    Function to load all important game variables from a fen string
    Example fen: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    """
    fen_string_pieces = fen.split(' ')
    load_from_fen_pieces(chess, fen_string_pieces[0])
    load_from_fen_player_to_move(chess, fen_string_pieces[1])    
    load_from_fen_castle(chess, fen_string_pieces[2])    