from AI import *
from board_processing import display_as_text  # for debugging, remove later
from board import check_line_clears


def half_holes(boardstate):
    out = []
    cb = board_to_col(boardstate_to_extended_boardstate(boardstate))
    for j, col in enumerate(cb[1:].split("/")):
        filled = False
        for i, cell in enumerate(col[::-1]):
            if cell == "." and filled == True:
                out.append((39-i, j))
            elif cell != "." and filled == False:
                filled = True
    return out


def bam(b, move):
    "Returns a the new boardstate after a move, without altering the original"
    return update_boardstate(copy(b), Piece(copy(move)))


def best_move(b, piece, hold):
    moves = find_possible_moves(b, piece, hold)
    msort = sorted(moves.keys(), key=lambda m: (
        len(half_holes(bam(b, m))), check_line_clears(bam(b, m)[1])))
    best_move = msort[0]
    # least_holes = float("inf")
    # contenders = []
    # best_move = ""
    # for move in moves.keys():
    #     holes = len(half_holes(bam(b, move)))
    #     if holes < least_holes:
    #         best_move = move
    #         least_holes = holes
    #         contenders = []
    #     elif holes == least_holes:
    #         contenders.append(move)
    if best_move == "":
        print("can't find best move")
        return moves[0]
    # if contenders != []:
    #     for m in contenders:

    # print(f"best move is {best_move} with {least_holes} holes")
    return moves[best_move]


if __name__ == "__main__":
    print(half_holes("*2ZIIII3/2ZZ6/3Z6"))
