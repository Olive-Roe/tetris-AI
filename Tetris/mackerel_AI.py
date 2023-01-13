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
    if hold == "":
        tm = find_theoretical_moves(b, piece)
    else:
        tm = find_theoretical_moves(b, piece) + find_theoretical_moves(b, hold)
    msort = sorted(tm, key=lambda m: (
        len(half_holes(bam(b, m))), check_line_clears(bam(b, m)[1])))
    best_move = msort[0]
    seq = pathfinding(b, Piece(best_move))
    if seq != False:  # if there exists a path
        return seq
    for i in range(len(msort)-1):
        seq = pathfinding(b, Piece(msort[i+1]))
        if seq != False:  # if there exists a path
            return seq
    return "none of the moves worl :("


if __name__ == "__main__":
    print(half_holes("*2ZIIII3/2ZZ6/3Z6"))
