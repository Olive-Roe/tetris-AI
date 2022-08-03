from time import sleep
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
    if int(piece.x) == 0:
        return ["L"]

    spawn = Piece(_return_spawn_piece_with_rotate(piece))
    x = spawn.x
    shift = int(piece.x) - x
    return FINESSE[shift]
    # if shift > 0:
    #     return ["r"]*shift
    # elif shift < 0:
    #     return ["l"]*(-1*shift)
    # else:
    #     return False


def optimise_finesse(seq):
    if seq == ["l", "l", "l"]:
        return ["L", "r"]


FINESSE = {'O0022': ['L'],
           'O0122': ['L', 'r'],
           'O0222': ['l', 'l'],
           'O0322': ['l'],
           'O0422': [],
           'O0522': ['r'],
           'O0622': ['r', 'r'],
           'O0722': ['R', 'l'],
           'O0822': ['R'],
           'O0922': [''],
           'O1022': [''],
           'O1122': [''],
           'O1222': [''],
           'O1322': [''],
           'O1422': [''],
           'O1522': [''],
           'O1622': [''],
           'O1722': [''],
           'O1822': [''],
           'O1922': [''],
           'O2022': [''],
           'O2122': [''],
           'O2222': [''],
           'O2322': [''],
           'O2422': [''],
           'O2522': [''],
           'O2622': [''],
           'O2722': [''],
           'O2822': [''],
           'O2922': [''],
           'O3022': [''],
           'O3122': [''],
           'O3222': [''],
           'O3322': [''],
           'O3422': [''],
           'O3522': [''],
           'O3622': [''],
           'O3722': [''],
           'O3822': [''],
           'O3922': [''],
           'T0022': ['L'],
           'T0122': ['l', 'l'],
           'T0222': ['l'],
           'T0322': [],
           'T0422': ['r'],
           'T0522': ['r', 'r'],
           'T0622': ['R', 'l'],
           'T0722': ['R'],
           'T0822': [''],
           'T0922': [''],
           'T1022': ['CW', 'L'],
           'T1122': ['L', 'CW'],
           'T1222': ['l', 'l', 'CW'],
           'T1322': ['l', 'CW'],
           'T1422': ['CW'],
           'T1522': ['r', 'CW'],
           'T1622': ['r', 'r', 'CW'],
           'T1722': ['R', 'l', 'CW'],
           'T1822': ['R', 'CW'],
           'T1922': [''],
           'T2022': [''],
           'T2122': ['180', 'L'],
           'T2222': ['180', 'l', 'l'],
           'T2322': ['180', 'l'],
           'T2422': ['180'],
           'T2522': ['180', 'r'],
           'T2622': ['180', 'r', 'r'],
           'T2722': ['180', 'R', 'l'],
           'T2822': ['180', 'R'],
           'T2922': [''],
           'T3022': [''],
           'T3122': ['L', 'CCW'],
           'T3222': ['l', 'l', 'CCW'],
           'T3322': ['l', 'CCW'],
           'T3422': ['CCW'],
           'T3522': ['r', 'CCW'],
           'T3622': ['r', 'r', 'CCW'],
           'T3722': ['R', 'l', 'CCW'],
           'T3822': ['R', 'CCW'],
           'T3922': ['CCW', 'R'],
           'I0022': ['L'],
           'I0122': ['l', 'l'],
           'I0222': ['l'],
           'I0322': [],
           'I0422': ['r'],
           'I0522': ['r', 'r'],
           'I0622': ['R'],
           'I0722': [''],
           'I0822': [''],
           'I0922': [''],
           'I1022': [''],
           'I1122': ['L', 'CW'],
           'I1222': [''],
           'I1322': ['l', 'CW'],
           'I1422': ['CW'],
           'I1522': [''],
           'I1622': [''],
           'I1722': ['R', 'CW'],
           'I1822': [''],
           'I1922': ['CW', 'R'],
           'I2022': [''],
           'I2122': [''],
           'I2222': [''],
           'I2322': [''],
           'I2422': [''],
           'I2522': [''],
           'I2622': [''],
           'I2722': [''],
           'I2822': [''],
           'I2922': [''],
           'I3022': ['CCW', 'L'],
           'I3122': [''],
           'I3222': ['L', 'CCW'],
           'I3322': [''],
           'I3422': [''],
           'I3522': ['CCW'],
           'I3622': ['r', 'CCW'],
           'I3722': [''],
           'I3822': ['R', 'CCW'],
           'I3922': [''],
           'S0022': ['L'],
           'S0122': ['l', 'l'],
           'S0222': ['l'],
           'S0322': [],
           'S0422': ['r'],
           'S0522': ['r', 'r'],
           'S0622': ['R', 'l'],
           'S0722': ['R'],
           'S0822': [''],
           'S0922': [''],
           'S1022': [''],
           'S1122': [''],
           'S1222': ['L', 'CW'],
           'S1322': [''],
           'S1422': [''],
           'S1522': ['CW'],
           'S1622': ['CW', 'r'],
           'S1722': ['CW', 'r', 'r'],
           'S1822': [''],
           'S1922': ['CW', 'R'],
           'S2022': [''],
           'S2122': [''],
           'S2222': [''],
           'S2322': [''],
           'S2422': [''],
           'S2522': [''],
           'S2622': [''],
           'S2722': [''],
           'S2822': [''],
           'S2922': [''],
           'S3022': [''],
           'S3122': ['CCW', 'L'],
           'S3222': [''],
           'S3322': ['CCW', 'l'],
           'S3422': ['CCW'],
           'S3522': [''],
           'S3622': [''],
           'S3722': [''],
           'S3822': ['R', 'CCW'],
           'S3922': [''],
           'Z0022': [''],
           'Z0122': ['L'],
           'Z0222': ['l', 'l'],
           'Z0322': ['l'],
           'Z0422': [],
           'Z0522': ['r'],
           'Z0622': ['r', 'r'],
           'Z0722': ['R', 'l'],
           'Z0822': ['R'],
           'Z0922': [''],
           'Z1022': [''],
           'Z1122': ['L', 'CW'],
           'Z1222': [''],
           'Z1322': [''],
           'Z1422': ['CW'],
           'Z1522': ['CW', 'r'],
           'Z1622': ['CW', 'r', 'r'],
           'Z1722': [''],
           'Z1822': ['CW', 'R'],
           'Z1922': [''],
           'Z2022': [''],
           'Z2122': [''],
           'Z2222': [''],
           'Z2322': [''],
           'Z2422': [''],
           'Z2522': [''],
           'Z2622': [''],
           'Z2722': [''],
           'Z2822': [''],
           'Z2922': [''],
           'Z3022': ['CCW', 'L'],
           'Z3122': [''],
           'Z3222': ['CCW', 'l'],
           'Z3322': ['CCW'],
           'Z3422': [''],
           'Z3522': [''],
           'Z3622': [''],
           'Z3722': ['R', 'CCW'],
           'Z3822': [''],
           'Z3922': [''],
           'J0022': ['L'],
           'J0122': ['l', 'l'],
           'J0222': ['l'],
           'J0322': [],
           'J0422': ['r'],
           'J0522': ['r', 'r'],
           'J0622': ['R', 'l'],
           'J0722': ['R'],
           'J0822': [''],
           'J0922': [''],
           'J1022': ['CW', 'L'],
           'J1122': ['L', 'CW'],
           'J1222': ['CW', 'l', 'l'],
           'J1322': ['CW', 'l'],
           'J1422': ['CW'],
           'J1522': ['CW', 'r'],
           'J1622': ['CW', 'r', 'r'],
           'J1722': ['CW', 'R', 'l'],
           'J1822': ['R', 'CW'],
           'J1922': [''],
           'J2022': [''],
           'J2122': [''],
           'J2222': ['L', '180'],
           'J2322': ['l', 'l', '180'],
           'J2422': ['l', '180'],
           'J2522': ['180'],
           'J2622': ['r', '180'],
           'J2722': ['r', 'r', '180'],
           'J2822': ['R', 'l', '180'],
           'J2922': ['R', '180'],
           'J3022': ['CCW', 'L'],
           'J3122': ['CCW', 'l', 'l'],
           'J3222': ['CCW', 'l'],
           'J3322': ['CCW'],
           'J3422': ['CCW', 'r'],
           'J3522': ['CCW', 'r', 'r'],
           'J3622': ['R', 'l', 'CCW'],
           'J3722': ['R', 'CCW'],
           'J3822': ['CCW', 'R'],
           'J3922': [''],
           'L0022': ['L'],
           'L0122': ['l', 'l'],
           'L0222': ['l'],
           'L0322': [],
           'L0422': ['r'],
           'L0522': ['r', 'r'],
           'L0622': ['R', 'l'],
           'L0722': ['R'],
           'L0822': [''],
           'L0922': [''],
           'L1022': ['CW', 'L'],
           'L1122': ['L', 'CW'],
           'L1222': ['CW', 'l', 'l'],
           'L1322': ['CW', 'l'],
           'L1422': ['CW'],
           'L1522': ['CW', 'r'],
           'L1622': ['CW', 'r', 'r'],
           'L1722': ['CW', 'R', 'l'],
           'L1822': ['R', 'CW'],
           'L1922': [''],
           'L2022': ['L', '180'],
           'L2122': ['l', 'l', '180'],
           'L2222': ['l', '180'],
           'L2322': ['180'],
           'L2422': ['r', '180'],
           'L2522': ['r', 'r', '180'],
           'L2622': ['R', 'l', '180'],
           'L2722': ['R', '180'],
           'L2822': [''],
           'L2922': [''],
           'L3022': [''],
           'L3122': ['CCW', 'L'],
           'L3222': ['CCW', 'l', 'l'],
           'L3322': ['CCW', 'l'],
           'L3422': ['CCW'],
           'L3522': ['CCW', 'r'],
           'L3622': ['CCW', 'r', 'r'],
           'L3722': ['R', 'l', 'CCW'],
           'L3822': ['R', 'CCW'],
           'L3922': ['CCW', 'R'], }

_REVERSE_TABLE = {"CW": "CCW", "CCW": "CW", "180": "180", "l": "r", "r": "l"}


def _get_reverse_action(action: str):
    if action not in _REVERSE_TABLE:
        raise ValueError(f"Bad argument: {action}")
    return _REVERSE_TABLE[action]


def kick_pathfinding(board: str, piece: Piece, seq=None):
    assert not _up_drop(board, piece)


def pathfinding(board: str, piece: Piece, seq=None):
    "Given a board and target piece, return sequence of actions to get the piece to there, or False if it's impossible"
    if seq is None:
        seq = []
    if not _up_drop(board, piece):
        # TODO: kicks/tucks pathfinding
        return False
    seq.insert(0, "hd")
    piece.update(f"{piece.type}{piece.orientation}{piece.x}{22}")
    seq = FINESSE[piece.value]
    if seq == ['']:
        return False
    seq.append("hd")
    return seq
    # r = _find_rotate(piece)
    # if r != False:
    #     # TODO: adjust for wall kicks
    #     # TODO: include DAS right/left (2-step finesse)
    #     # TODO: remove symmetrical positions (s/z/i)
    #     seq.insert(0, r)
    #     pb, kick = rotate_and_update(
    #         construct_piece_board_notation(piece.value, board), r)
    #     p, b = separate_piece_board_notation(pb)
    #     piece2 = Piece(p)

    # x = _find_x_shift(piece)
    # if x != False:
    #     # insert each x shift into sequence
    #     for i in x:
    #         seq.insert(-1, i)
    # return seq
    # # try actions


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


def find_kicks(z="*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/"):
    oL = []
    for piecetype in list("IJLOSTZ"):
        # pathfind
        d = find_possible_moves(z, piecetype, "Z")
        # find all places piece can land
        e = find_theoretical_moves(z, piecetype)
        test = [x for x in e if x not in d and find_sym(x) not in d]
        for x in test:
            if find_sym(x) in test:
                test.remove(x)
        oL += test
    return oL


def main():
    global t, screen
    t, screen = init_screen(600)
    print(find_kicks())
    # z = "*JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS/"
    # # a = board_to_bw(z)
    # d = find_possible_moves(z, "J", "L")
    # test_moves(z, d)
    # print(d)
    # print(faildict)
    # e = find_theoretical_moves(z, "Z")
    # # print(e)
    # # print(d)
    # print([x for x in e if x not in d and find_sym(x) not in d])
    # # # test_move(z, "S034", ["CCW", 'l', 'hd'])


if __name__ == "__main__":
    main()
