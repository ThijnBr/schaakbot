from tkinter import Frame, Button, Tk
from board.chess_board import Chess
from undo_functions.undo_main import undo_move

class ChessGUI:
    def __init__(self, root, chess):
        self.root = root
        self.chess = chess

        self.frm = Frame(root)
        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        self.old_click = None

        self.create_board_gui()
        self.create_undo_button()

    def undo(self):
        undo_move(chess)
        self.update_board_gui()

    def create_undo_button(self):
        button = Button(self.frm, text='Undo', bg='white', width=8, height=2, command=self.undo)
        button.grid(row=8, column=0, columnspan=8)

    def create_board_gui(self):
        for i in range(8):
            for j in range(8):
                piece = self.chess.board[i][j]
                bg_color = 'white' if (i + j) % 2 == 0 else 'brown'
                text = str(piece) if piece else ''
                button = Button(self.frm, text=text, bg=bg_color, width=8, height=4)
                button.grid(row=i, column=j)
                button.config(command=lambda row=i, col=j: self.button_click(row, col))
                self.buttons[i][j] = button

    def update_board_gui(self):
        for i in range(8):
            for j in range(8):
                piece = self.chess.board[i][j]
                text = str(piece) if piece else ''
                self.buttons[i][j].config(text=text)

    def reset_button_colors(self):
        for i in range(8):
            for j in range(8):
                bg_color = 'white' if (i + j) % 2 == 0 else 'brown'
                self.buttons[i][j].config(bg=bg_color)

    def button_click(self, y, x):
        self.reset_button_colors()

        current_piece = self.chess.board[y][x]

        # If old_click is set and current_piece belongs to current turn
        if self.old_click is not None:
            old_y, old_x = self.old_click
            selected_piece = self.chess.board[old_y][old_x]

            if selected_piece and selected_piece.color == self.chess.current_turn:
                if self.chess.make_move((old_y, old_x), (y, x)):
                    self.update_board_gui()

                self.old_click = None
                return

        # Highlight possible moves if a piece of the current turn is selected
        if current_piece and current_piece.color == self.chess.current_turn:
            self.old_click = (y, x)
            possible_positions = current_piece.get_possible_moves((y, x), self.chess)
            for pos_y, pos_x in possible_positions:
                self.buttons[pos_y][pos_x].config(bg='green')

root = Tk()
chess = Chess('rnbqkbnr/pppp2pp/4pp2/8/8/4PN2/PPPPBPPP/RNBQK2R b KQkq - 1 3') 
gui = ChessGUI(root, chess)
gui.frm.pack()
root.mainloop()
