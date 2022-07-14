import itertools
from board_processing import boardstate_to_extended_boardstate, display_as_text
from updating_board import update_boardstate, _get_coord_list
from piece import Piece
import storage


def board_to_bw(board):
    "Converts a board to black and white, x for filled cells and . for unfilled cells"
    # remove starting asterisk
    eb = boardstate_to_extended_boardstate(board)[1:]
    return "*" + "/".join(["".join([c if c == "." else "x" for c in row]) for row in eb.split("/")])


def board_to_col(board):
    "Converts a board into a string split by columns instead of rows"
    oL = [[] for _ in range(10)]
    # remove starting asterisk, split by row
    for row in board[1:].split("/"):
        for index, c in enumerate(row):
            oL[index].append(c)
    return "*" + "/".join(["".join(l) for l in oL])


def _find_floor(board):
    "Given a board notation, returns a list of coordinates (x, y) of empty cells with filled cells directly underneath."
    oL = []
    col_form = board_to_col(boardstate_to_extended_boardstate(board))
    # remove starting asterisk, split by column
    for x, col in enumerate(col_form[1:].split("/")):
        # set the floor as filled
        prev = "x"
        # iterating upwards in a column
        for y, cell in enumerate(col):
            if cell == "." and prev != ".":
                oL.append((x, y))
            prev = cell
    return oL


def find_theoretical_moves(board: str, piecetype: str):
    "Find all locations for a piece given a board (that may not be accessible)"
    oL = []
    targets = _find_floor(board)
    # check both current piece and held piece
    for target_square in targets:
        tx, ty = target_square
        for orientation in range(4):
            offsets = storage.blc_offsets[piecetype][orientation]
            for off in offsets:
                # find reverse offsets
                rx, ry = -off[0], -off[1]
                # find original blc
                blcx, blcy = (tx+rx, ty+ry)
                message = f"{piecetype}{orientation}{blcx}{blcy}"
                if update_boardstate(board, Piece(message)) not in ["out of bounds", "occupied cell"] and message not in oL:
                    oL.append(message)
    return oL


def pathfinding(board: str, piece: Piece):
    "Given a board and target piece, return sequence of actions to get the piece to there, or False if it's impossible"
    # TODO: A* algorithm from target location to spawn
    pass


# def find_possible_moves2(board: str, piece: str):
#     # worst case fallback: iterating 400 times for all possibilities
#     return [f"{piece}{orientation}{x}{y}" for x, y, orientation in itertools.product(range(10), range(20), range(4)) if update_boardstate(board, Piece(f"{piece}{orientation}{x}{y}")) not in ["out of bounds", "occupied cell"] and update_boardstate(board, Piece(f"{piece}{orientation}{x}{y-1}")) in ["out of bounds", "occupied cell"]]


if __name__ == "__main__":
    z = "*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/"
    a = board_to_bw(z)
    print(find_theoretical_moves("*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/", "T"))
