class Chess:
    def __init__(self):        
        self.board = [['. ' for _ in range(8)] for _ in range(8)]
        self.turn = 0
        self.last_move = None
        self.initialize_pieces()

    def change_turn(self):
        self.turn = 1 - self.turn
        if self.is_checkmate(self.turn):
            print("Checkmate")
        if self.is_in_check(self.turn):
            print("Check!")

    def initialize_pieces(self):
        pieces_black = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
        pieces_white = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK']

        #Pionnen
        for y in range(8):
            self.board[1][y] = pieces_white[0]
            self.board[6][y] = pieces_black[0]

        #Torens
        self.board[0][0] = pieces_white[1]
        self.board[0][7] = pieces_white[1]
        self.board[7][0] = pieces_black[1]
        self.board[7][7] = pieces_black[1]

        #Paarden
        self.board[0][1] = pieces_white[2]
        self.board[0][6] = pieces_white[2]
        self.board[7][1] = pieces_black[2]
        self.board[7][6] = pieces_black[2]

        #Lopers
        self.board[0][2] = pieces_white[3]
        self.board[0][5] = pieces_white[3]
        self.board[7][2] = pieces_black[3]
        self.board[7][5] = pieces_black[3]

        #Koninginnen
        self.board[0][3] = pieces_white[4]
        self.board[7][3] = pieces_black[4]

        #Koningen
        self.board[0][4] = pieces_white[5]
        self.board[7][4] = pieces_black[5]

    def is_in_bounds(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8
    
    def is_empty(self, x, y):
        return self.board[y][x] == '. '
    
    def is_enemy(self, x, y, color):
        if color == 'w':
            return self.board[y][x][0] == 'b'
        else:
            return self.board[y][x][0] == 'w'
        
    def pawn_movement(self, color, x, y):
        possible_positions = []
        direction = 1 if color == 'w' else -1
        start_row = 1 if color == 'w' else 6
        en_passant_row = 5 if color == 'w' else 2

        if self.last_move != None:
            last_from, last_to, last_piece = self.last_move

        #move forward one or two positions based on start position
        if self.is_in_bounds(x, y + direction) and self.is_empty(x, y + direction):
            possible_positions.append((x, y + direction))
            if y == start_row and self.is_empty(x, y + 2 * direction):
                possible_positions.append((x, y + 2 * direction))

        #diagonall captures
        for dx in [-1, 1]:
            new_x = x + dx
            new_y = y+direction
            if self.is_in_bounds(new_x, new_y) and self.is_enemy(new_x, new_y, color):
                possible_positions.append((new_x, new_y))
            if self.last_move != None:
                if abs(last_to[1] - last_from[1]) == 2 and last_piece[1] == 'P' and y+direction == en_passant_row and new_x == last_from[0]:
                    possible_positions.append((new_x, new_y))

        return possible_positions
    
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
        return self.single_movement(color, x, y, king_moves)
    
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

    
    def move_piece(self, piece, old_position, new_position):
        old_x, old_y = old_position
        x, y = new_position

        if (self.turn == 0 and piece[0] == 'w') or (self.turn == 1 and piece[0] == 'b'):
            if new_position in self.check_moveable_positions(piece, old_position):
                if piece[1] == 'P' and abs(old_x - x) == 1:
                    self.board[y + (-1 if piece[0] == 'w' else 1)][x] = '. '
                self.board[old_y][old_x] = '. '
                self.board[y][x] = piece
                self.last_move = (old_position, new_position, piece)
                self.change_turn()

    def print_board(self):
        for row in reversed(self.board):
            print(' '.join(piece for piece in row))
