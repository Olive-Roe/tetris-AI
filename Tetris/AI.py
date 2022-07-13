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
    col_form = board_to_col(board)
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


def find_possible_moves(board: str, piecetype: str, held_piece: str):
    # worst case fallback: iterating 400 times for all possibilities
    return [f"{piecetype}{orientation}{x}{y}" for x, y, orientation in itertools.product(range(10), range(20), range(4)) if update_boardstate(board, Piece(f"{piecetype}{orientation}{x}{y}")) not in ["out of bounds", "occupied cell"] and update_boardstate(board, Piece(f"{piecetype}{orientation}{x}{y-1}")) in ["out of bounds", "occupied cell"]]


new_dict = {}
for piece in storage.blc_table:
    new_dict[piece] = [[], [], [], []]
    for orientation in range(4):
        blx, bly = storage.blc_table[piece][orientation]
        center_offset_list = storage.offset_list_table[piece][orientation]
        for offset in center_offset_list:
            offx, offy = offset
            new_dict[piece][orientation].append((offx+2-blx, offy+2-bly))
print(new_dict)

if __name__ == "__main__":
    pass
    # a = board_to_bw("*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/")
    # print(find_possible_moves("*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/", "T", "O"))
    # display_as_text(a)
    # b = board_to_col(a)
    # # print(b)
    # c = _find_floor(a)
    # print(c)
    # print(_get_coord_dict(Piece("T000")))
