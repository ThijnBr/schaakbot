from piece.sub_pieces import King
from undo_functions.undo_main import undo_move
from board.load_fen import load_from_fen
from castling.castling_main import castling_move, check_castling_move
from castling.castling_check_for_movement import check_for_king_movement, check_for_rook_movement

class Chess:
    def __init__(self, fen=None):
        self.board = [[None for _ in range(8)] for _ in range(8)]

        #startSquare, targetSquare, targetPiece, 
        #bool isLongCastle = false, bool isShortCastle = False, 
        # isFirstKingMove = False, isFirstRookMove = False, 
        # TODO ENPASSANT
        self.history = []

        self.castle_short_white = False
        self.castle_long_white = False
        self.castle_short_black = False
        self.castle_long_black = False

        self.white_king_moved = False
        self.black_king_moved = False

        self.black_rook_long_moved = False
        self.black_rook_short_moved = False
        self.white_rook_long_moved = False
        self.white_rook_short_moved = False

        self.current_turn = None

        if fen:
            load_from_fen(self, fen)
        else:
            load_from_fen(self, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def print_board(self):
        for row in self.board:
            print(" ".join([str(piece) if piece else '--' for piece in row]))
    
    #check if coordinates inside board
    def is_in_bounds(self, y, x):
        return 0 <= x < 8 and 0 <= y < 8
    
    #check if position has no piece
    def is_empty(self, y, x):
        return self.board[y][x] == None
    
    #check if position is enemy
    def is_enemy(self, y, x, color):
        piece = self.board[y][x]
        if piece != None:
            return piece.color != color
    
    def is_in_check(self, color):
        # Find the position of the king
        king_position = self.find_king_position(color)
        if not king_position:
            return False

        # Check if any of the opponent's pieces attacks the king
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and self.is_enemy(y, x, color):
                    possible_moves = piece.get_possible_moves((y, x), self, 1)
                    if king_position in possible_moves:
                        return True
        
        return False

    def find_king_position(self, color):
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    return (y, x)
        return None

    def make_move(self, start, end):
        start_y, start_x = start
        end_y, end_x = end

        piece = self.board[start_y][start_x]
        target_piece = self.board[end_y][end_x]
        
        if end in piece.get_possible_moves(start, self, move=1):
            is_short_castle = False
            is_long_castle = False
            is_first_rook_move = False
            first_king_move = False

            if check_castling_move(piece, start_x, end_x):
                is_short_castle, is_long_castle = castling_move(self, piece, end_x)
            else:
                self.board[end_y][end_x] = piece
                self.board[start_y][start_x] = None

            first_king_move = check_for_king_movement(self, piece, first_king_move)
            is_first_rook_move = check_for_rook_movement(self, piece, start, is_first_rook_move)

            move = (start, end, target_piece, is_short_castle, is_long_castle, first_king_move, is_first_rook_move)
            self.history.append(move)

            self.switch_turn()
            return True
        return False
    
        
    def filter_moves(self, possible_moves, piece, position):
        valid_moves = []
        for move in possible_moves:
            # Temporarily simulate the move
            self.make_move(position, move)

            # Check if the move leaves the king in check
            if not self.is_in_check(piece.color):
                valid_moves.append(move)

            # Reset the board state after simulation
            undo_move(self)

        return valid_moves

    