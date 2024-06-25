from piece.sub_pieces import King
from undo_functions.undo_main import undo_move
from board.load_fen import load_from_fen
from castling.castling_main import castling_move, check_castling_move
from castling.castling_check_for_movement import check_for_king_movement, check_for_rook_movement
from en_passant.en_passant_main import setup_en_passant, check_for_en_passant_capture, en_passant_capture_move
from promotion.promotion_main import check_for_promotion, promote_piece
from algorithms.minmax import standard_minimax

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
        (bool) isEnPassantCapture = False
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
    
    def is_checkmate(self, color):
        """
        params:
        (string) color
        
        Function to check if the given color is in checkmate.

        Returns:
        bool: True if the given color is in checkmate, False otherwise.
        """
        all_moves = []
        
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece and piece.color == color:
                    possible_moves = piece.get_possible_moves((y, x), self)
                    all_moves += possible_moves
        
        if all_moves == []:
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
    
    def make_ai_move(self, depth):
        maximizing_player = True if self.current_turn == 'white' else False
        evaluation, move = standard_minimax(self, depth, maximizing_player)
        if move:
            self.make_move(move[0], move[1])

    def make_move(self, start, end, promotion_piece=None):
        """
        params:
        (tuple) start
        (tuple) end

        Function to make a move on the board. Order of functions for it to work correctly.
        1. check if move is en passant capture
        2. move/capture functions
        3. setup en passant for next move
        4. check if promotion is possible based on current board state
        5. check if there was any rook or king movement
        6. append move to history
        7. switch turns
        """
        start_y, start_x = start
        end_y, end_x = end

        # Piece that is moved
        piece = self.board[start_y][start_x]
        # Piece that is potentially captured
        target_piece = self.board[end_y][end_x]
        
        # Initialize variables
        is_short_castle, is_long_castle, is_first_rook_move, first_king_move, en_passant_piece, en_passant_capture, promotion = False, False, False, False, None, False, False

        # Check if en passant move is possible
        en_passant_capture = check_for_en_passant_capture(self, piece, start_x, end_y, end_x)

        if en_passant_capture:
            en_passant_capture_move(self, start_y, start_x, end_y, end_x)
        # Check if move is castling move
        elif check_castling_move(piece, start_x, end_x):
            is_short_castle, is_long_castle = castling_move(self, piece, end_x)
        # Default move
        else:
            self.default_move(piece, start_y, start_x, end_y, end_x)

        # Setup en passant for next move
        en_passant_piece = setup_en_passant(self, piece, start_y, end_y, end_x)

        # Check if piece can be promoted.
        promotion_possible = check_for_promotion(piece, end_y)
        if promotion_possible:
            promotion = True
            promote_piece(self, end_y, end_x, promotion_piece)

        # Check if its a first piece move
        first_king_move = check_for_king_movement(self, piece, first_king_move)
        is_first_rook_move = check_for_rook_movement(self, piece, start, is_short_castle, is_long_castle, is_first_rook_move)

        # Tuple for history
        move = (start, end, target_piece, is_short_castle, is_long_castle, first_king_move, is_first_rook_move, en_passant_piece, en_passant_capture, promotion)
        self.history.append(move)

        self.switch_turn()
    
    def default_move(self, piece, start_y, start_x, end_y, end_x):
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