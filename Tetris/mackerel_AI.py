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


def hole_coveredness(b):
    cb = board_to_col(boardstate_to_extended_boardstate(b))
    out = []
    for col in cb[1:].split("/"):
        hole = False
        covers = 0
        for cell in col:
            if cell == "." and hole == False:
                hole = True
            elif cell != "." and hole:
                covers += 1
        out.append(covers)
    return out


def _stack_heights(b):
    cb = board_to_col(boardstate_to_extended_boardstate(b))
    out = []
    for col in cb[1:].split("/"):
        for i, cell in enumerate(col[::-1]):
            if cell != ".":
                out.append(40-i)
                break
        else:
            out.append(0)
    return out


def shd(b):
    "Returns the stack height differences"
    sh = _stack_heights(b)
    out = []
    for i in range(9):
        out.append(abs(sh[i] - sh[i+1]))
    return out


def sum_shd_exc_well(b, column_no):
    "Return the sum of the stack height differences excluding a certain column number"
    d = shd(b)
    # removes the two shd to the left and right of the removed well
    if column_no == 0:
        d.pop(0)
    elif column_no == 9:
        d.pop(8)
    else:
        d.pop(column_no-1)
        d.pop(column_no-1)
    return sum(d)


def highest_stack(b):
    return max(_stack_heights(b))


def sum_shd_exc_lowest(b):
    "Return the sum of the stack height differences excluding the lowest column"
    # done in one go for performance
    # TODO: test performance w/ list slicing/numpy
    sh = _stack_heights(b)
    _, idx = min((low, idx) for (idx, low) in enumerate(sh))
    return sum_shd_exc_well(b, idx)
    # out = []
    # for i in range(9):
    #     if i != low or i+1 != low:
    #         out.append(abs(sh[i] - sh[i+1]))
    # return out


def parity_diff(b, excl_col=""):
    # min = 0, max = 10, norm = /10
    out = []
    sh = _stack_heights(b)
    for index, item in enumerate(sh):
        # make performance better
        if excl_col != "" and sh != excl_col:
            out.append((item % 2) ^ (index % 2))
            # xor of column number mod 2 and stack height mod 2
    # harder to read list comprehension below
    # [(item % 2)^(index % 2) for index, item in enumerate(sh) if sh != excl_col]
    return abs(out.count(1) - out.count(0))


def pd_exc_lowest(b):
    # min = 0, max = 9, norm = /10
    sh = _stack_heights(b)
    _, idx = min((low, idx) for (idx, low) in enumerate(sh))
    return parity_diff(b, idx)


def cleanliness(b, weights=""):
    "Returns a value from 0 to 1 on how clean the board is"
    if weights == "":
        weights = []
    out = 0
    return 0  # this ai makes quite dirty stacks


def best_move(b, piece, hold, queue):
    if hold == "":
        hold = queue[0]
    tm = find_theoretical_moves(b, piece) + find_theoretical_moves(b, hold)

    def order(m):
        nb = bam(b, m)
        return (-1*check_line_clears(nb)[1], len(half_holes(nb)),  sum(hole_coveredness(nb)), highest_stack(nb), sum_shd_exc_lowest(nb), pd_exc_lowest(nb))
    msort = sorted(tm, key=order)
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
