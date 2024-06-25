class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.image_path = None

    def __repr__(self):
        return f"{self.color[0].upper()}{self.name[0].upper()}"
    
    def get_possible_moves(self, position, chess, move=0) -> list:
        """
        params:
        (Tuple (y, x)) position
        (class Chess) chess
        (int) move: Indicating the context of move calculation:
            - 0: Normal move calculation, filter out positions that leave the king in check.
            - 1: Calculation done within the context of checking if the current player's king is in check.

        Function to check all possible moves. First get all moves, then filter out positions that are in check.

        Returns:
        list: A list of tuples with all possible positions the piece can move to.
        """
        possible_positions = self.get_all_moves(position, chess)
        if move == 0:
            filtered_positions = chess.filter_moves(possible_positions, self, position)
            return filtered_positions
        return possible_positions


    def linear_movement(self, y, x, moves, board):
        """
        params:
        (int) y
        (int) x
        (list of tuples) moves
        (3D list) board

        Function to get possible positions with a linear loop. For bishops, queens and rooks

        Returns:
        list: A list of tuples with all possible positions.
        """
        possible_positions = []
        for move_y, move_x in moves:
            new_y, new_x = y + move_y, x + move_x
            while board.is_in_bounds(new_y, new_x):
                if board.is_empty(new_y, new_x):
                    possible_positions.append((new_y, new_x))
                elif board.is_enemy(new_y, new_x, self.color):
                    possible_positions.append((new_y, new_x))
                    break
                else:
                    break
                new_x += move_x
                new_y += move_y
        return possible_positions

    def single_movement(self, y, x, moves, board):
        """
        params:
        (int) y
        (int) x
        (list of tuples) moves
        (3D list) board

        Function to get possible positions with a single loop. For pieces as King and Knight

        Returns:
        list: A list of tuples with all possible positions.
        """
        possible_positions = []
        for dy, dx in moves:
            new_y, new_x = y + dy, x + dx
            if board.is_in_bounds(new_y, new_x):
                if board.is_empty(new_y, new_x) or board.is_enemy(new_y, new_x, self.color):
                    possible_positions.append((new_y, new_x))
        return possible_positions