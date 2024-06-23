from piece.piece_main import Piece

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'pawn')
        self.en_passant = False

    def get_all_moves(self, position, chess):
        """
        params:
        (Tuple) position
        (class Chess) chess

        Function to calculate all moves which are possibble for the Pawn. Includes captures.

        Returns:
        list: A list of tuples with all possible positions.
        """
        possible_positions = []
        y, x = position
        direction = 1 if self.color == 'black' else -1
        start_row = 1 if self.color == 'black' else 6
        
        # Forward movement
        if chess.is_in_bounds(y + direction, x) and chess.is_empty(y + direction, x):
            possible_positions.append((y + direction, x))
            if y == start_row and chess.is_empty(y + 2 * direction, x):
                possible_positions.append((y + 2 * direction, x))

        # Capture moves
        capture_moves = [(direction, -1), (direction, 1)]
        for dy, dx in capture_moves:
            ny, nx = y + dy, x + dx
            if chess.is_in_bounds(ny, nx):
                # Normal capture
                if chess.is_enemy(ny, nx, self.color):
                    possible_positions.append((ny, nx))

                # En passant capture
                # if chess.is_in_bounds(y, nx):
                #     adjacent_piece = chess.board[y][nx]
                #     if isinstance(adjacent_piece, Pawn) and adjacent_piece.color != self.color and adjacent_piece.en_passant:
                #         possible_positions.append((ny, nx))

        return possible_positions

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'rook')

    def get_all_moves(self, position, board):
        """
        params:
        (Tuple) position
        (class Chess) chess

        Function to calculate all moves which are possibble for the Rook. Includes captures.

        Returns:
        list: A list of tuples with all possible positions.
        """
        x, y = position
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        possible_positions = self.linear_movement(x, y, moves, board)
        return possible_positions


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'knight')

    def get_all_moves(self, position, board):
        """
        params:
        (Tuple) position
        (class Chess) chess

        Function to calculate all moves which are possibble for the Knight. Includes captures.

        Returns:
        list: A list of tuples with all possible positions.
        """
        x, y = position
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]  # Knight's possible moves
        possible_positions = self.single_movement(x, y, moves, board)
        return possible_positions


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'bishop')

    def get_all_moves(self, position, board):
        """
        params:
        (Tuple) position
        (class Chess) chess

        Function to calculate all moves which are possibble for the Bishop. Includes captures.

        Returns:
        list: A list of tuples with all possible positions.
        """
        x, y = position
        moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions
        possible_positions = self.linear_movement(x, y, moves, board)
        return possible_positions

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'queen')

    def get_all_moves(self, position, board):
        """
        params:
        (Tuple) position
        (class Chess) chess

        Function to calculate all moves which are possibble for the Queen. Includes captures.

        Returns:
        list: A list of tuples with all possible positions.
        """
        x, y = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Rook directions
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Bishop directions
        possible_positions = self.linear_movement(x, y, directions, board)
        return possible_positions


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'king')

    def get_all_moves(self, position, chess):
        """
        params:
        (Tuple) position
        (class Chess) chess

        Function to calculate all moves which are possibble for the King. Includes captures.

        Returns:
        list: A list of tuples with all possible positions.
        """
        x, y = position
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Vertical and Horizontal
                 (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal
        possible_positions = self.single_movement(x, y, moves, chess)
        
        # Get the castle positions
        self.castle_positions(chess, possible_positions)
        
        return possible_positions
    
    def castle_positions(self, chess, possible_positions):
        """
        params:
        (class Chess) chess
        (list of tuples) possible_positions

        Function to calculate the castle positions and appending them to possible_positions.
        """
        # Check if black or white castle
        y = 7 if self.color == 'white' else 0

        # Get rook for short castle
        rook_short = chess.board[y][7]
        # Get rook for long castle
        rook_long = chess.board[y][0]
        
        king_moved = chess.white_king_moved if self.color == 'white' else chess.black_king_moved
        castle_short = chess.castle_short_white if self.color == 'white' else chess.castle_short_black
        castle_long = chess.castle_long_white if self.color == 'white' else chess.castle_long_black
        
        # Check for short castling
        if rook_short and not king_moved and castle_short and chess.is_empty(y,5) and chess.is_empty(y,6):
            possible_positions.append((y,6))

        # Check for long castling
        if rook_long and not king_moved and castle_long and chess.is_empty(y,1) and chess.is_empty(y,2) and chess.is_empty(y,3):
            possible_positions.append((y,2))