from time import sleep
from board_processing import separate_piece_board_notation
from updating_board import rotate_and_update
from game import init_screen
from board_processing import boardstate_to_extended_boardstate, display_as_text
from updating_board import update_boardstate, _combine_coordlists, construct_piece_board_notation
from piece import Piece
from board import Board, draw_grid
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
            # skip orientations of O
            if piecetype == "O" and orientation != 0:
                continue
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


def _up_drop(board: str, piece: Piece):
    """Takes a board and a piece, and tries to move the piece upwards as much as possible.
    If it can move all the way to y=22, this function will return True"""
    # iterate from current y to 22
    for y in range(piece.y, 23):
        test = update_boardstate(board, Piece(
            f"{piece.type}{piece.orientation}{piece.x}{y}"))
        if test in ["out of bounds", "occupied cell"]:
            return f"{piece.type}{piece.orientation}{piece.x}{y-1}"
    return True


def _find_rotate(piece: Piece):
    "Given a piece, find the rotation it takes to get it from spawn orientation to its current orientation"
    if piece.orientation == 0:
        # should not happen
        return False
    elif piece.orientation == 1:
        return "CW"
    elif piece.orientation == 2:
        return "180"
    elif piece.orientation == 3:
        return "CCW"


def _find_x_shift(piece: Piece):
    x = 3 if piece.type in ["L", "J", "S", "T", "I"] else 4
    shift = int(piece.x) - x
    if shift > 0:
        return ["r"]*shift
    elif shift < 0:
        return ["l"]*(-1*shift)
    else:
        return False


def pathfinding(board: str, piece: Piece, seq=None):
    "Given a board and target piece, return sequence of actions to get the piece to there, or False if it's impossible"
    if seq is None:
        seq = []
    if not (ud := _up_drop(board, piece)):
        # TODO: kicks/tucks pathfinding
        return False
    seq.insert(0, "hd")
    piece.update(f"{piece.type}{piece.orientation}{piece.x}{22}")
    x = _find_x_shift(piece)
    if x != False:
        # insert each x shift into sequence
        for i in x:
            seq.insert(0, i)
    r = _find_rotate(piece)
    if r != False:
        # TODO: adjust for wall kicks
        seq.insert(0, r)
        pb, kick = rotate_and_update(
            construct_piece_board_notation(piece.value, board), r)
        p, b = separate_piece_board_notation(pb)
        piece = Piece(p)
    return seq
    # try actions


def find_possible_moves(board: str, piecetype: str, held_piecetype: str):
    oD = {}
    for piece in [piecetype, held_piecetype]:
        moves = find_theoretical_moves(board, piece)
        for m in moves:
            seq = pathfinding(board, Piece(m))
            if seq != False:  # if there exists a path
                oD[m] = seq
    return oD


def _return_spawn_piece(piece: Piece):
    if piece.type in ["L", "J", "S", "T", "I"]:
        x, y = 3, 22
    elif piece.type in ["Z", "O"]:
        x, y = 4, 22
    return f"{piece.type}{piece.orientation}{x}{y}"


def test_move(board, piece, actions):
    b = Board(t, screen, _return_spawn_piece(Piece(piece)), board)
    b.do_actions_from_input("\n".join(actions))
    if b.piece.value == piece:
        print(f"{piece} works")
    else:
        print(f"{piece} fail")


faildict = {'T104': ['l', 'l', 'CW', 'hd'], 'T114': ['l', 'l', 'CW', 'hd'], 'T214': ['l', 'l', 'l', '180', 'hd'], 'T314': ['l', 'l', 'CCW', 'hd'], 'T124': ['l', 'CW', 'hd'], 'T224': ['l', 'l', '180', 'hd'], 'T324': ['l', 'CCW', 'hd'], 'T134': ['CW', 'hd'], 'T243': ['180', 'hd'], 'T234': ['l', '180', 'hd'], 'T343': ['r', 'CCW', 'hd'], 'T334': ['CCW', 'hd'], 'T040': ['r', 'hd'], 'T140': ['r', 'CW', 'hd'], 'T350': ['r', 'r', 'CCW', 'hd'], 'T151': [
    'r', 'r', 'CW', 'hd'], 'T162': ['r', 'r', 'r', 'CW', 'hd'], 'T251': ['r', '180', 'hd'], 'T262': ['r', 'r', '180', 'hd'], 'T362': ['r', 'r', 'r', 'CCW', 'hd'], 'T173': ['r', 'r', 'r', 'r', 'CW', 'hd'], 'T273': ['r', 'r', 'r', '180', 'hd'], 'T373': ['r', 'r', 'r', 'r', 'CCW', 'hd'], 'T184': ['r', 'r', 'r', 'r', 'r', 'CW', 'hd'], 'T284': ['r', 'r', 'r', 'r', '180', 'hd'], 'T384': ['r', 'r', 'r', 'r', 'r', 'CCW', 'hd'], 'T394': ['r', 'r', 'r', 'r', 'r', 'CCW', 'hd']}


def test_moves(board, dict):
    for piece, actions in dict.items():
        b = Board(t, screen, _return_spawn_piece(Piece(piece)), board)
        b.do_actions_from_input("\n".join(actions))
        # draw_grid(update_boardstate(z, Piece(piece)), t, screen)
        # sleep(0.5)
        # TODO: highlight target piece location
        if b.piece.value == piece:
            print(f"{piece} works")
        else:
            print(f"{piece} fail")
            faildict[piece] = actions
# def find_possible_moves2(board: str, piece: str):
#     # worst case fallback: iterating 400 times for all possibilities
#     return [f"{piece}{orientation}{x}{y}" for x, y, orientation in itertools.product(range(10), range(20), range(4)) if update_boardstate(board, Piece(f"{piece}{orientation}{x}{y}")) not in ["out of bounds", "occupied cell"] and update_boardstate(board, Piece(f"{piece}{orientation}{x}{y-1}")) in ["out of bounds", "occupied cell"]]


if __name__ == "__main__":
    t, screen = init_screen()
    z = "*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/"
    # a = board_to_bw(z)
    # print(find_theoretical_moves(z, "T"))
    d = find_possible_moves(z, "T", "O")
    test_moves(z, d)
    print(faildict)
    # b = Board(t, screen, "T0322")
