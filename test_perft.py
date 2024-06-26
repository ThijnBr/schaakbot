from board.chess_board import Chess
from undo_functions.undo_main import undo_move
from piece.sub_pieces import Rook, Bishop, Queen, Knight, Pawn

available_promotion_piece = [Rook, Bishop, Queen, Knight]
def perft(chess, depth):
    if depth == 0 or chess.is_checkmate(chess.current_turn):
        return 1

    total_moves = 0
    current_turn = chess.current_turn
    promotion_rank = 0 if current_turn == 'white' else 7

    for y in range(8):
        for x in range(8):
            piece = chess.board[y][x]

            if piece and piece.color == current_turn:
                piece_moves = piece.get_possible_moves((y, x), chess)

                for new_pos in piece_moves:
                    old_pos = (y, x)

                    if isinstance(piece, Pawn) and new_pos[0] == promotion_rank:
                        for promotion_piece in available_promotion_piece:
                            chess.make_move(old_pos, new_pos, promotion_piece(current_turn))
                            sub_total_moves = perft(chess, depth - 1)
                            total_moves += sub_total_moves
                            undo_move(chess)
                    else:
                        chess.make_move(old_pos, new_pos)
                        sub_total_moves = perft(chess, depth - 1)
                        total_moves += sub_total_moves
                        undo_move(chess)

    return total_moves
default_board_perft_values = [1, 20, 400, 8902, 197281]
castle_board_perft_values = [1, 26, 749, 19718]
castle_short_board_perft_values = [1, 29, 776]
en_passant_board_perft_values = [1, 6, 104, 639]
en_passant_board2_perft_values = [1, 14, 191, 2812, 43238]
promotion_board_perft_values = [1, 6, 264, 9467]
debug_board_perft_values = [1, 25, 1067, 28108]

def test_perft(chess_fen, expected_perft_values, depth, description):
    chess = Chess(chess_fen)
    for i in range(depth):
        total_moves = perft(chess, i)
        if total_moves == expected_perft_values[i]:
            print(f"{description} perft {i} completed: success")
        else:
            print(f"perft {i} completed: failed. total_moves = {total_moves}")

def main():
    # test_perft('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', default_board_perft_values, 4, 'Default board')
    # print()
    # test_perft('rnbqkbnr/pppp2pp/4pp2/8/8/4PN2/PPPPBPPP/RNBQK2R b KQkq - 1 3', castle_board_perft_values, 3, 'Castle board')
    # print()
    # test_perft('rnbqkbnr/pppp3p/4ppp1/8/8/4PN2/PPPPBPPP/RNBQK2R w KQkq - 0 4', castle_short_board_perft_values, 3, 'Castle short board')
    # print()
    # test_perft('4k3/8/8/8/K1p4r/8/1P/8 w -', en_passant_board_perft_values, 4, 'En passant board')
    # print()
    # test_perft('8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - ', en_passant_board2_perft_values, 4 ,'En passant board 2')
    # print()
    # test_perft('r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1', promotion_board_perft_values, 4, 'Promotion board')
    # print()
    test_perft('rnbqk1nr/pppp1ppp/8/8/4P3/2N5/PP3PPP/R1BQKB1R b KQkq - 0 6', debug_board_perft_values, 4, 'debug board')    

if __name__ == "__main__":
    main()
