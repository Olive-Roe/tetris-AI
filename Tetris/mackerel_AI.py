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


def cleanliness(b):
    "Returns a value from 0 to 1 on how clean the board is"
    return 0 # this ai makes quite dirty stacks


def best_move(b, piece, hold, queue):
    if hold == "":
        hold = queue[0]
    tm = find_theoretical_moves(b, piece) + find_theoretical_moves(b, hold)
    msort = sorted(tm, key=lambda m: (
        len(half_holes(bam(b, m))), check_line_clears(bam(b, m)[1])))
    best_move = msort[0]
    seq = pathfinding(b, Piece(best_move))
    if seq != False:  # if there exists a path
        if best_move[0] == hold:
            return ["hold"] + seq
        return seq
    for i in range(len(msort)-1):
        seq = pathfinding(b, Piece(msort[i]))
        if seq != False:  # if there exists a path
            if best_move[0] == hold:
                return ["hold"] + seq
            return seq
    raise ValueError("none of the moves work :(")


if __name__ == "__main__":
    print(half_holes("*2ZIIII3/2ZZ6/3Z6"))
