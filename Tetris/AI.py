from time import sleep
from copy import copy
from board_processing import separate_piece_board_notation
from updating_board import rotate_and_update
from game import init_screen
from board_processing import boardstate_to_extended_boardstate, display_as_text
from updating_board import update_boardstate, _combine_coordlists, construct_piece_board_notation, _find_rotation_direction
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
    # TODO: Prune output of this for obviously covered places (I pieces in garbage lines)
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
                if blcx < 0 or blcx > 9 or blcy < 0 or blcy > 39:
                    # hacky out of bounds check
                    continue
                message = f"{piecetype}{orientation}{blcx}{blcy}"
                # FIXME: Piece('T2106') (x=10) is interpreted as Piece('T216')
                if update_boardstate(board, Piece(message)) not in ["out of bounds", "occupied cell"] and message not in oL:
                    oL.append(message)
    return oL


def _up_drop(board: str, piece: Piece):
    """Takes a board and a piece, and tries to move the piece upwards as much as possible.
    Returns the final Piece (stops at 22)"""
    # iterate from current y to 22
    piece = copy(piece)
    for y in range(piece.y, 23):
        test = update_boardstate(board, Piece(
            f"{piece.type}{piece.orientation}{piece.x}{y}"))
        if test in ["out of bounds", "occupied cell"]:
            return Piece(f"{piece.type}{piece.orientation}{piece.x}{y-1}")
    return Piece(f"{piece.type}{piece.orientation}{piece.x}22")


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


_REVERSE_TABLE = {"CW": "CCW", "CCW": "CW",
                  "180": "180", "l": "r", "r": "l", "hd": "hd", "ud": "d"}


def _get_reverse_action(action: str):
    # TODO: Soft drop the exact amount needed instead of all the way
    if action not in _REVERSE_TABLE:
        raise ValueError(f"Bad argument: {action}")
    return _REVERSE_TABLE[action]


def do_action(board: str, piece: str, action):
    "Takes a board, piece string, and action, and returns the updated piece"
    temp_b = Board("", "", piece, board)
    if action == "ud":
        return _up_drop(board, Piece(piece)).value
    temp_b.do_action(action)
    return temp_b.piece.value


def kick_pathfinding(board: str, piece: str):
    """Uses BFS to find the sequence of moves to get to a location in a board
    Returns the sequence and the final piece"""
    visited = [piece]
    queue = [[]]
    while True:
        # Check whether to give up
        if not queue:  # if queue is empty list, everything has been checked
            return False, Piece(piece)
        item = queue[0]
        tpiece = piece
        if item != []:
            # initialise current piece with actions
            for action in item:
                tpiece = do_action(board, tpiece, action)
        # Check is search is finished (can move up to y=22)
        test_piece = _up_drop(board, Piece(tpiece))
        if test_piece.y == 22:
            # TODO: Find exact amount to drop piece by
            # y_diff = 22 - Piece(tpiece).y
            # # hacky fix because y_diff is sometimes negative?
            # if y_diff < 0:
            #     y_diff = ""
            #  Gets current item (action list)
            # Reverse all actions and order (this searches from target location, so sequence is reversed)
            # message = [f"d{y_diff}"] + [_REVERSE_TABLE[i] for i in item][::-1]
            message = ["d"] + [_REVERSE_TABLE[i] for i in item][::-1]
            # TODO: clean up temporary piece names
            # Check that all the actions are reversible
            # t3piece -> (actions) -> piece
            t3piece = copy(tpiece)
            for action in message:
                t3piece = do_action(board, t3piece, action)
            if t3piece == piece:
                # checked, ready to send
                return message, Piece(tpiece)
        for action in ["CW", "CCW", "180", "l", "r", "ud"]:
            # Create temporary piece
            t2piece = do_action(board, tpiece, action)
            if t2piece != piece and t2piece not in visited:
                # Adds action to item and adds to back
                queue.append(item + [action])
                visited.append(t2piece)
        queue.pop(0)


def pathfinding(board: str, piece: Piece):
    "Given a board and target piece, return sequence of actions to get the piece to there, or False if it's impossible"
    # Initialise empty list for possible kick sequence
    kick_seq = []
    if _up_drop(board, piece).y != 22:
        kick_seq, piece = kick_pathfinding(board, piece.value)
    if kick_seq is False:
        return False
    piece.update(f"{piece.type}{piece.orientation}{piece.x}{22}")
    # Shallowly copied because kicks mess up the original?
    seq = copy(storage.finesse[piece.value])
    if seq == ['']:
        return False
    seq += kick_seq
    seq.append("hd")
    return seq


def find_possible_moves(board: str, piecetype: str, held_piecetype: str):
    oD = {}
    for piece in [piecetype, held_piecetype]:
        # TODO: Add 'hold' to the start of the held piece's actions
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
    return f"{piece.type}{0}{x}{y}"


def _return_spawn_piece_with_rotate(piece: Piece):
    "Given a Piece, return the spawn piece value after rotation"
    if piece.type in ["L", "J", "S", "T", "I"]:
        x, y = 3, 22
    elif piece.type in ["Z", "O"]:
        x, y = 4, 22
    if piece.orientation == 0:
        return f"{piece.type}{0}{x}{y}"
    new_piece = Piece(f"{piece.type}{0}{x}{y}")
    direction = _find_rotation_direction(piece.orientation)
    pb, kick = rotate_and_update(
        construct_piece_board_notation(new_piece.value, "*"), direction)
    p, b = separate_piece_board_notation(pb)
    return p


def test_move(board, piece, actions):
    b = Board(t, screen, _return_spawn_piece(Piece(piece)), board)
    b.do_actions_from_input("\n".join(actions))
    if b.piece.value == piece:
        print(f"{piece} works")
    else:
        print(f"{piece} fail")
        print(f"actual: {b.piece.value}")
    screen.exitonclick()


# faildict = {'T104': ['l', 'l', 'CW', 'hd'], 'T114': ['l', 'l', 'CW', 'hd'], 'T214': ['l', 'l', 'l', '180', 'hd'], 'T314': ['l', 'l', 'CCW', 'hd'], 'T124': ['l', 'CW', 'hd'], 'T224': ['l', 'l', '180', 'hd'], 'T324': ['l', 'CCW', 'hd'], 'T134': ['CW', 'hd'], 'T243': ['180', 'hd'], 'T234': ['l', '180', 'hd'], 'T343': ['r', 'CCW', 'hd'], 'T334': ['CCW', 'hd'], 'T040': ['r', 'hd'], 'T140': ['r', 'CW', 'hd'], 'T350': ['r', 'r', 'CCW', 'hd'], 'T151': [
#    'r', 'r', 'CW', 'hd'], 'T162': ['r', 'r', 'r', 'CW', 'hd'], 'T251': ['r', '180', 'hd'], 'T262': ['r', 'r', '180', 'hd'], 'T362': ['r', 'r', 'r', 'CCW', 'hd'], 'T173': ['r', 'r', 'r', 'r', 'CW', 'hd'], 'T273': ['r', 'r', 'r', '180', 'hd'], 'T373': ['r', 'r', 'r', 'r', 'CCW', 'hd'], 'T184': ['r', 'r', 'r', 'r', 'r', 'CW', 'hd'], 'T284': ['r', 'r', 'r', 'r', '180', 'hd'], 'T384': ['r', 'r', 'r', 'r', 'r', 'CCW', 'hd'], 'T394': ['r', 'r', 'r', 'r', 'r', 'CCW', 'hd']}
# {'T104': ['l', 'l', 'CW', 'hd'], 'T114': ['l', 'l', 'CW', 'hd'], 'T214': ['l', 'l', 'l', '180', 'hd'], 'T314': ['l', 'l', 'CCW', 'hd'], 'T124': ['l', 'CW', 'hd'], 'T224': ['l', 'l', '180', 'hd'], 'T324': ['l', 'CCW', 'hd'], 'T134': ['CW', 'hd'], 'T243': ['180', 'hd'], 'T234': ['l', '180', 'hd'], 'T343': ['r', 'CCW', 'hd'], 'T334': ['CCW', 'hd'], 'T040': ['r', 'hd'], 'T140': ['r', 'CW', 'hd'], 'T350': ['r', 'r', 'CCW', 'hd'], 'T151': ['r', 'r', 'CW', 'hd'], 'T162': ['r', 'r', 'r', 'CW', 'hd'], 'T251': ['r', '180', 'hd'], 'T262': ['r', 'r', '180', 'hd'], 'T362': ['r', 'r', 'r', 'CCW', 'hd'], 'T173': ['r', 'r', 'r', 'r', 'CW', 'hd'], 'T273': ['r', 'r', 'r', '180', 'hd'], 'T373': ['r', 'r', 'r', 'r', 'CCW', 'hd'], 'T184': ['r', 'r', 'r', 'r', 'r', 'CW', 'hd'], 'T284': ['r', 'r', 'r', 'r', '180', 'hd'], 'T384': ['r', 'r', 'r', 'r', 'r', 'CCW', 'hd'], 'T394': ['r', 'r', 'r', 'r', 'r', 'CCW', 'hd']}
faildict = {}


def test_moves(board, dict):
    for piece, actions in dict.items():
        b = Board(t, screen, _return_spawn_piece(
            Piece(piece)), board)
        b.do_actions_from_input("\n".join(actions))
        # draw_grid(update_boardstate(z, Piece(piece)), t, screen)
        # sleep(0.5)
        # TODO: highlight target piece location
        if b.piece.value == piece:
            print(f"{piece} works")
        else:
            print(f"{piece} fail, actual: {b.piece.value}")
            faildict[piece] = actions
# def find_theoretical_moves2(board: str, piece: str):
#     # worst case fallback: iterating 400 times for all possibilities
#     return [f"{piece}{orientation}{x}{y}" for x, y, orientation in itertools.product(range(10), range(20), range(4)) if update_boardstate(board, Piece(f"{piece}{orientation}{x}{y}")) not in ["out of bounds", "occupied cell"] and update_boardstate(board, Piece(f"{piece}{orientation}{x}{y-1}")) in ["out of bounds", "occupied cell"]]


def find_sym(piece):
    if piece[0] == "O":
        return f"{piece[0]}0{piece[2:]}"
    if piece[0] in list("ZSI"):
        return piece[0]+str((int(piece[1])-2) % 4)+piece[2:]
    return ""


def test_kicks(board):
    oL = []
    for piecetype, held_piecetype in [("I", "O"), ("J", "L"), ("S", "Z"), ("T", "O")]:
        # pathfind
        d = find_possible_moves(board, piecetype, held_piecetype)
        test_moves(board, d)
        # find all places piece can land
        e = find_theoretical_moves(board, piecetype)
        test = [x for x in e if x not in d and find_sym(x) not in d]
        for x in test:
            if find_sym(x) in test:
                test.remove(x)
        oL += test
    return oL


def main():
    b = "*g3/g3/g3/g3/g3/OO1LLLIJJJ/OO1SSLIJZZ/J3SSIZZI/J2TTTIOOI/JJ1LTZZOOI/3LZZZSSI/2LL2ZZSS/7Z2"
    d = find_possible_moves(b, "T", "J")
    test_moves(b, d)
    print(faildict)
    # {'T2106': ['180', 'L', 'hd'], 'T3106': ['L', 'CCW', 'hd'], 'J120': ['CW', 'L', 'd', 'CCW', 'CCW', '180', 'hd']}
    # z = "*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/"
    # print(test_kicks(z))
    # # a = board_to_bw(z)
    # d = find_possible_moves(z, "J", "T")
    # test_moves(z, d)
    # print(d)
    # print(faildict)
    # e = find_theoretical_moves(z, "Z")
    # # print(e)
    # # print(d)
    # print([x for x in e if x not in d and find_sym(x) not in d])
    # # # test_move(z, "S034", ["CCW", 'l', 'hd'])


if __name__ == "__main__":
    t, screen = init_screen(600)
    main()
