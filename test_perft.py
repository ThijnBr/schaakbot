from board.chess_board import Chess
from undo_functions.undo_main import undo_move

def perft(chess, depth):
    if depth == 0:
        return 1

    total_moves = 0
    current_turn = chess.current_turn
    
    for y in range(8):
        for x in range(8):
            piece = chess.board[y][x]
            if piece and piece.color == current_turn:
                piece_moves = piece.get_possible_moves((y, x), chess)
                for new_pos in piece_moves:
                    old_pos = (y, x)
                    #print(f'{old_pos}:{new_pos}')
                    chess.make_move(old_pos, new_pos)
                    total_moves += perft(chess, depth - 1)
                    undo_move(chess)

    return total_moves

default_board_perft_values = [1, 20, 400, 8902, 197281, 4865609]
castle_board_perft_values = [1, 26, 749, 19718, 587091]
castle_short_board_perft_values = [1, 29, 776]

def main_test():
    chess = Chess('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    for x in range(5):
        total_moves = perft(chess, x)
        if total_moves == default_board_perft_values[x]:
            print(f'perft {x} completed: success')
        else:
            print(f'perft {x} completed: failed. total_moves = {total_moves}')

def castle_test():
    chess = Chess('rnbqkbnr/pppp2pp/4pp2/8/8/4PN2/PPPPBPPP/RNBQK2R b KQkq - 1 3')
    for x in range(3):
        total_moves = perft(chess, x)
        if total_moves == castle_board_perft_values[x]:
            print(f'perft castle {x} completed: success')
        else:
            print(f'perft castle {x} completed: failed. total_moves = {total_moves}')

def castle_test_short():
    chess = Chess('rnbqkbnr/pppp3p/4ppp1/8/8/4PN2/PPPPBPPP/RNBQK2R w KQkq - 0 4')
    for x in range(3):
        total_moves = perft(chess, x)
        if total_moves == castle_short_board_perft_values[x]:
            print(f'perft castle short {x} completed: success')
        else:
            print(f'perft castle short {x} completed: failed. total_moves = {total_moves}')

def main():
    main_test()
    print()
    castle_test()
    print()
    castle_test_short()

def debug():
    chess = Chess('rnbqkbnr/pppp3p/4ppp1/8/8/4PN2/PPPPBPPP/RNBQK2R w KQkq - 0 4')
    total_moves = perft(chess, 1)
    print(total_moves)

if __name__ == "__main__":
    main()
