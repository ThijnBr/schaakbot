from tkinter import Frame, Button, Tk
from chessStructure import Chess

class ChessGUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board

        self.frm = Frame(root)
        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        self.old_click = None

        self.create_board_gui()

    def create_board_gui(self):
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                bg_color = 'white' if (i + j) % 2 == 0 else 'brown'
                text = piece if piece != '. ' else ''
                button = Button(self.frm, text=text, bg=bg_color, width=8, height=4)
                button.grid(row=i, column=j)
                button.config(command=lambda row=i, col=j: self.button_click(row, col))
                self.buttons[i][j] = button

    def update_board_gui(self):
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                text = piece if piece != '. ' else ''
                self.buttons[i][j].config(text=text)

    def reset_button_colors(self):
        for i in range(8):
            for j in range(8):
                bg_color = 'white' if (i + j) % 2 == 0 else 'brown'
                self.buttons[i][j].config(bg=bg_color)

    def button_click(self, y, x):
        self.reset_button_colors()

        current_piece = self.board.board[y][x]

        # Check if it's a valid selection or move
        if self.old_click is not None:
            old_x, old_y = self.old_click
            selected_piece = self.board.board[old_y][old_x]

            

            # Check if the old click had a piece and it's the correct player's turn
            if selected_piece != '. ' and ((self.board.turn == 0 and selected_piece[0] == 'w') or (self.board.turn == 1 and selected_piece[0] == 'b')):
                # Current clicked position
                new_x, new_y = x, y

                # Move the piece on the board if the move is valid
                if (new_x, new_y) in self.board.check_moveable_positions(selected_piece, (old_x, old_y)):
                    self.board.move_piece(selected_piece, (old_x, old_y), (new_x, new_y))
                    self.board.ai_move(depth=2)
                    self.update_board_gui()
                    self.old_click = None  # Reset old click after move
                    return

        # Set the new old_click position if the selected piece is valid
        if current_piece != '. ' and ((self.board.turn == 0 and current_piece[0] == 'w') or (self.board.turn == 1 and current_piece[0] == 'b')):
            self.old_click = (x, y)
            possible_positions = self.board.check_moveable_positions(current_piece, (x, y))
            for pos in possible_positions:
                pos_x, pos_y = pos
                self.buttons[pos_y][pos_x].config(bg='green')

root = Tk()
board = Chess()
gui = ChessGUI(root, board)
gui.frm.pack()
root.mainloop()
