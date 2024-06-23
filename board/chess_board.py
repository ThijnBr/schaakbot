from piece.sub_pieces import King
from undo_functions.undo_main import undo_move
from board.load_fen import load_from_fen
from castling.castling_main import castling_move, check_castling_move
from castling.castling_check_for_movement import check_for_king_movement, check_for_rook_movement
from en_passant.en_passant_main import check_en_passant_possible, check_for_en_passant_capture, en_passant_capture_move

class Chess:
    def __init__(self, fen=None):
        self.board = [[None for _ in range(8)] for _ in range(8)]

        """ 
        Content of history list

        (tuple) startSquare
        (tuple) targetSquare
        (class Piece) targetPiece
        (bool) isLongCastle = False
        (bool) isShortCastle = False
        (bool) isFirstKingMove = False
        (bool) isFirstRookMove = False
        (bool) isEnPassantPossible = False
        (bool) isEnPassantSkipped = False
        """
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

        self.en_passant_target = None

        self.current_turn = None

        if fen:
            load_from_fen(self, fen)
        else:
            load_from_fen(self, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def print_board(self):
        for row in self.board:
            print(" ".join([str(piece) if piece else '--' for piece in row]))

    def switch_turn(self):
        """
        Function to switch turns
        """
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
    
    def is_in_bounds(self, y, x):
        """
        params:
        (int) y
        (int) x

        Function to check if position is inside board

        Returns:
        bool
        """
        return 0 <= x < 8 and 0 <= y < 8
    
    def is_empty(self, y, x):
        """
        params:
        (int) y
        (int) x

        Function to check if position is empty

        Returns:
        bool
        """
        return self.board[y][x] == None
    
    def is_enemy(self, y, x, color):
        """
        params:
        (int) y
        (int) x
        (string) color

        Function to check if position is enemy

        Returns:
        bool
        """
        piece = self.board[y][x]
        if piece != None:
            return piece.color != color
    
    def is_in_check(self, color):
        """
        params:
        (string) color
        
        Function to check if the king positions is in check.

        Returns:
        bool: False if no king or not in check. True if in check.
        """
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
        """
        params:
        (string) color

        Function to find the position of the king

        Returns:
        Tuple: (y, x) or None if no king found
        """
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    return (y, x)
        return None

    def make_move(self, start, end):
        """
        params:
        (tuple) start
        (tuple) end

        Function to make a move on the board.
        """
        start_y, start_x = start
        end_y, end_x = end

        # Piece that is moved
        piece = self.board[start_y][start_x]
        # Piece that is potentially captured
        target_piece = self.board[end_y][end_x]
        
        # Initialize variables
        is_short_castle, is_long_castle, is_first_rook_move, first_king_move, en_passant_target, en_passant_capture = False, False, False, False, None, False

        # Make the move on the board
        en_passant_capture = check_for_en_passant_capture(self, piece, end_y, end_x, self.current_turn)
        if en_passant_capture:
            en_passant_capture_move(self, start_y, start_x)
        if check_castling_move(piece, start_x, end_x):
            is_short_castle, is_long_castle = castling_move(self, piece, end_x)
        else:
            self.default_capture(piece, start_y, start_x, end_y, end_x)
        
        # Check if its a first piece move
        first_king_move = check_for_king_movement(self, piece, first_king_move)
        is_first_rook_move = check_for_rook_movement(self, piece, start, is_first_rook_move)

        # Check if en passant is possible for opponent and get target piece
        en_passant_target = check_en_passant_possible(self, piece, start_y, end_y, end_x)
        self.en_passant_target = en_passant_target

        # Tuple for history
        move = (start, end, target_piece, is_short_castle, is_long_castle, first_king_move, is_first_rook_move, en_passant_target, en_passant_capture)
        self.history.append(move)

        self.switch_turn()
    
    def default_capture(self, piece, start_y, start_x, end_y, end_x):
        """
        params:
        (class Piece) piece
        (int) start_y
        (int) start_x
        (int) end_y
        (int) end_x
        """
        self.board[end_y][end_x] = piece
        self.board[start_y][start_x] = None
        
    def filter_moves(self, possible_moves, piece, position):
        """
        params:
        (list) possible_moves
        (class Piece) piece
        (tuple (y, x) position
        """
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