from chessSolver import minimax
import copy

class Chess():
    def __init__(self):        
        self.board = None
        self.turn = 0
        self.last_move = None

        self.points = {
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9
        }
        
        #castling
        self.castle_white = [1,1]
        self.castle_black = [1,1]

        self.initialize_pieces()
    
    def copy(self):
        # Return a deep copy of the current game state
        return copy.deepcopy(self)

    def ai_move(self, depth):
        if self.turn == 1:
            _, (piece, old_pos, new_pos) = minimax(self.copy(), depth, False)
            print(f'stuk:{piece}:')
            self.move_piece(piece, old_pos, new_pos)

    def change_turn(self):
        self.turn = 1 - self.turn
        if self.is_checkmate(self.turn):
            print("Checkmate")
        if self.is_in_check(self.turn):
            print("Check!")

    def initialize_pieces(self, fen=None):
        self.board = [['. ' for _ in range(8)] for _ in range(8)]
        if fen:
            self.load_fen(fen)
        else:
            self.set_default_position()

    def set_default_position(self):
        self.load_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def load_fen(self, fen):
        rows = fen.split()[0].split('/')
        for x, row in enumerate(rows):
            y = 0
            for char in row:
                if char.isdigit():
                    y += int(char)
                else:
                    piece = ('w' if char.isupper() else 'b') + char.upper()
                    self.board[x][y] = piece
                    y += 1

    #check if coordinates inside board
    def is_in_bounds(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8
    
    #check if position has no piece
    def is_empty(self, x, y):
        return self.board[y][x] == '. '
    
    #check if position is enemy
    def is_enemy(self, x, y, color):
        if color == 'w':
            return self.board[y][x][0] == 'b'
        else:
            return self.board[y][x][0] == 'w'
        
    def pawn_movement(self, color, x, y):
        possible_positions = []
        direction = 1 if color == 'b' else -1
        start_row = 1 if color == 'b' else 6
        
        #move forward one or two positions based on start position
        if self.is_in_bounds(x, y + direction) and self.is_empty(x, y + direction):
            possible_positions.append((x, y + direction))
            if y == start_row and self.is_empty(x, y + 2 * direction):
                possible_positions.append((x, y + 2 * direction))

        self.pawn_captures(x,y, direction, color, possible_positions)

        return possible_positions
    
    def pawn_captures(self, x, y, direction, color, possible_positions):
        en_passant_row = 5 if color == 'b' else 2
        if self.last_move != None:
            last_from, last_to, last_piece = self.last_move[:3]
        #diagonall captures
        for dx in [-1, 1]:
            new_x = x + dx
            new_y = y+direction
            if self.is_in_bounds(new_x, new_y) and self.is_enemy(new_x, new_y, color):
                possible_positions.append((new_x, new_y))
            if self.last_move != None:
                if abs(last_to[1] - last_from[1]) == 2 and last_piece[1] == 'P' and y+direction == en_passant_row and new_x == last_from[0]:
                    possible_positions.append((new_x, new_y))

    def rook_movement(self, color, x ,y):
        #rook directions
        rook_moves = [[0,1],[0,-1],[1,0],[-1,0]]
        return self.linear_movement(color, x, y, rook_moves)
    
    def bishop_movement(self, color, x ,y):
        #bishop directions
        bishop_moves = [[1,1],[-1,-1],[-1,1],[1,-1]]
        return self.linear_movement(color, x, y, bishop_moves)
    
    def knight_movement(self, color, x, y):
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        return self.single_movement(color, x, y, knight_moves)
    
    def queen_movement(self, color, x, y):
        return self.bishop_movement(color, x, y) + self.rook_movement(color, x, y)
    
    def king_movement(self, color, x, y):
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        possible_positions = self.single_movement(color, x, y, king_moves)

        if color == 'b' and (x == 4 and y == 0) and self.is_empty(5, 0) and self.is_empty(6,0) and self.castle_white[0] == 1:
            possible_positions.append((6,0))
        if color == 'b' and (x == 4 and y == 0) and self.is_empty(3,0) and self.is_empty(2,0) and self.is_empty(1,0) and self.castle_white[1] == 1:
            possible_positions.append((2,0))
        if color == 'w' and (x == 4 and y == 7) and self.is_empty(5, 7) and self.is_empty(6,7) and self.castle_black[0] == 1:
            possible_positions.append((6,7))
        if color == 'w' and (x == 4 and y == 7) and self.is_empty(3,0) and self.is_empty(2,0) and self.is_empty(1,0) and self.castle_black[1] == 1:
            possible_positions.append((2,7))

        return possible_positions
    
    def filter_positions_check(self, possible_positions, piece, x, y):
        filtered_positions = []
        for pos in possible_positions:
            old_piece = self.board[y][x]
            self.board[y][x] = '. '
            new_x, new_y = pos
            captured_piece = self.board[new_y][new_x]
            self.board[new_y][new_x] = piece

            if not self.is_in_check(self.turn):
                filtered_positions.append(pos)

            self.board[y][x] = old_piece
            self.board[new_y][new_x] = captured_piece

        return filtered_positions

    def linear_movement(self, color, x, y, moves):
        possible_positions = []
        for move_x, move_y in moves:
            #add x and y from possible move in direction
            new_x, new_y = x + move_x, y + move_y
            while self.is_in_bounds(new_x, new_y):
                if self.is_empty(new_x, new_y):
                    possible_positions.append((new_x, new_y))
                elif self.is_enemy(new_x, new_y, color):
                    possible_positions.append((new_x, new_y))
                    break
                else:
                    break
                new_x += move_x
                new_y += move_y
        return possible_positions
    
    def single_movement(self, color, x, y, moves):
        possible_positions = []
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if self.is_in_bounds(new_x, new_y):
                if self.is_empty(new_x, new_y) or self.is_enemy(new_x, new_y, color):
                    possible_positions.append((new_x, new_y))
        return possible_positions



    def check_moveable_positions(self, piece, position, move=0):
        possible_positions = []
        x, y = position

        if piece == '. ':
            return

        piece_type = piece[1]
        color = piece[0]

        piece_types = {
            'P': self.pawn_movement,
            'R': self.rook_movement,
            'N': self.knight_movement,
            'B': self.bishop_movement,
            'Q': self.queen_movement,
            'K': self.king_movement
        }

        if piece_type in piece_types:
            possible_positions = piece_types[piece_type](color, x, y)

        if move == 0:
            possible_positions = self.filter_positions_check(possible_positions, piece, x, y)
                        
        return possible_positions
    
    def is_checkmate(self, turn):
        position = self.find_king_position(turn)
        piece = 'wK' if turn == 0 else 'bK'
        if self.check_moveable_positions(piece, position) == [] and self.is_in_check(turn):
            return True
        else:
            return False
    
    def is_in_check(self, turn):
        king_position = self.find_king_position(turn)
        opponent = 'b' if turn == 0 else 'w'
        return self.is_king_under_threat(king_position, opponent)

    def find_king_position(self, turn):
        king_piece = 'wK' if turn == 0 else 'bK'
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == king_piece:
                    return (x, y)
        return None

    def is_king_under_threat(self, king_position, opponent):
        for y in range(8):
            for x in range(8):
                if self.board[y][x][0] == opponent:
                    if self.can_piece_attack_king(self.board[y][x], (x, y), king_position):
                        return True
        return False

    def can_piece_attack_king(self, piece, piece_position, king_position):
        return king_position in self.check_moveable_positions(piece, piece_position, 1)

    # Checks if the performed move impacts castling.
    def check_castle(self, piece, x):
        if piece[1] == 'K':
            if self.turn == 0:
                self.castle_white = [0, 0]
            else:
                self.castle_black = [0, 0]
        elif piece[1] == 'R':
            if self.turn == 0:
                if x < 4:
                    self.castle_white[1] = 0  # Disable Queen side castle for white
                elif x > 4:
                    self.castle_white[0] = 0  # Disable King side castle for white
            else:
                if x < 4:
                    self.castle_black[1] = 0  # Disable Queen side castle for black
                elif x > 4:
                    self.castle_black[0] = 0 # Disable King side castle for black
    
    def en_passant(self, piece, old_x, x, y):
        if piece[1] == 'P' and abs(old_x - x) == 1:
            self.board[y + (-1 if piece[0] == 'b' else 1)][x] = '. '
    
    def move_piece(self, piece, old_position, new_position):
        old_x, old_y = old_position
        x, y = new_position

        if (self.turn == 0 and piece[0] == 'w') or (self.turn == 1 and piece[0] == 'b'):
            if new_position in self.check_moveable_positions(piece, old_position):
                # Check for castling
                if piece == 'wK' and abs(old_x - x) == 2:
                    if x == 6:  # Kingside castling
                        self.perform_castling(0, 4, 5, 6, 'wR', 'wK')
                    elif x == 2:  # Queenside castling
                        self.perform_castling(0, 4, 3, 2, 'wR', 'wK')
                elif piece == 'bK' and abs(old_x - x) == 2:
                    if x == 6:  # Kingside castling
                        self.perform_castling(7, 4, 5, 6, 'bR', 'bK')
                    elif x == 2:  # Queenside castling
                        self.perform_castling(7, 4, 3, 2, 'bR', 'bK')
                else:
                # Normal moves
                    captured_piece = None if self.board[y][x] == '. ' else self.board[y][x]
                    if captured_piece != None:
                        print(captured_piece)
                    self.board[old_y][old_x] = '. '
                    self.board[y][x] = piece

                    # Special moves
                    self.check_castle(piece, x)
                    self.en_passant(piece, old_x, x, y)
                    
                    self.last_move = (old_position, new_position, piece, captured_piece, self.castle_white[:], self.castle_black[:])
                    self.change_turn()

    def perform_castling(self, row, king_start, rook_start, king_end, rook, king):
        captured_piece = self.board[row][king_end]
        self.last_move = ((row, king_start), (row, king_end), king, captured_piece, self.castle_white[:], self.castle_black[:])

        self.board[row][king_start] = '. '
        self.board[row][rook_start] = rook
        self.board[row][king_end] = king
        self.board[row][7] = '. '

        if king_start < king_end:  # Kingside castling
            if row == 0:
                self.castle_white[0] = 0
            else:
                self.castle_black[0] = 0
        else:  # Queenside castling
            if row == 0:
                self.castle_white[1] = 0
            else:
                self.castle_black[1] = 0


    def print_board(self):
        for row in reversed(self.board):
            print(' '.join(piece for piece in row))
