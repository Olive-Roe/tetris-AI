import storage
from piece import Piece
from board_processing import *
from typing import List


def _combine_coordlists(pieces: List[Piece]):
    "Given a list of Pieces, generate a dict of coordinates with all the pieces, giving the earliest pieces most priority"
    # Might be a bit inefficient (4n) for n number of pieces
    output_dict = {}
    for piece in pieces:
        coord_dict = _get_coord_dict(piece)
        for key, value in coord_dict.items():
            if key not in output_dict.keys():
                output_dict[key] = value
    return output_dict


def _get_coord_dict(piecestate: Piece):
    # Check whether the piece is an O piece and set its orientation to 0 (doesn't matter in updating boardstate)
    if piecestate.type == "O":
        piecestate = Piece(f"O0{str(piecestate.x)}{str(piecestate.y)}")
    # Gets a list of offsets from the Piece
    offset_list = _find_offset_list(piecestate)
    # Finds the center x and y coordinates
    center_x, center_y = _find_center(piecestate)
    # Combining offset and center list to find the list of the actual coordinates
    return {k: piecestate.type for k in [(x_offset + center_x, y_offset + center_y) for (x_offset, y_offset) in offset_list]}


def _get_coord_list(piecestate: Piece):
    # Check whether the piece is an O piece and set its orientation to 0 (doesn't matter in updating boardstate)
    if piecestate.type == "O":
        piecestate = Piece(f"O0{str(piecestate.x)}{str(piecestate.y)}")
    # Gets a list of offsets from the Piece
    offset_list = _find_offset_list(piecestate)
    # Finds the center x and y coordinates
    center_x, center_y = _find_center(piecestate)
    # Combining offset and center list to find the list of the actual coordinates
    return [(x_offset + center_x, y_offset + center_y) for (x_offset, y_offset) in offset_list]


def _find_center(piecestate: Piece):
    'Given a Piece, returns the coordinates of its actual center (x, y)'
    blx, bly = _findBLC(piecestate)
    # The x-offset from the actual x of the piece to the center is 2-blx, same for y
    # Therefore, the center is x+2-blx
    return piecestate.x + 2 - blx, piecestate.y + 2 - bly


def _find_offset_list(piecestate: Piece):
    'Given a Piece, returns a list of offsets of each filled tile from the center [(x1, y1), (x2, y2)]'
    # Note: .upper() is used in case of ghost pieces
    return storage.offset_list_table[piecestate.type.upper()][piecestate.orientation]


def _find_blc_offset(piecestate: Piece):
    pass


def update_boardstate(boardstate, piecestate: Piece, coord_dict=""):
    '''Takes a boardstate and a Piece, and returns the boardstate with the piece in it, or "out of bounds/occupied cell" if it is impossible
    If coord_dict is given, this surpasses piecestate, and updates the boardstate with the given coord_dict.'''
    # Immediate check whether the piece is out of bounds (to save time)
    if piecestate.x < 0 or piecestate.x > 9 or piecestate.y < 0 or piecestate.y > 39:
        return "out of bounds"
    if coord_dict == "":
        coord_dict = _get_coord_dict(piecestate)
    # Creates a temporary extended boardstate
    nbs = boardstate_to_extended_boardstate(boardstate)
    # Loops over each tile to check whether they are allowed
    for xy, piece_type in coord_dict.items():
        x_loc, y_loc = xy
        # If the x/y coordinates are higher/lower than the size of the board
        if x_loc < 0 or x_loc > 9 or y_loc < 0 or y_loc > 39:
            return "out of bounds"
        # If the cell is empty
        if access_cell(boardstate, y_loc, x_loc) == ".":
            # Updates the cell with the piece type (e.g. T)
            nbs = change_cell(nbs, y_loc, x_loc, piece_type)
        else:
            return "occupied cell"
    # Turn back into abbreviated boardstate
    return extended_boardstate_to_boardstate(nbs)


def update_boardstate_from_pb_notation(pb_notation):
    'Takes a piece-board notation and returns the updated board notation'
    p1, b1 = separate_piece_board_notation(pb_notation)
    return update_boardstate(b1, Piece(p1))


def _findBLC(piece: Piece):
    'Given a shape, finds its bottom left corner relative to a 5x5 grid (helper function to update_boardstate)'
    # Note: .upper() is used in case of ghost pieces
    return storage.blc_table[piece.type.upper()][piece.orientation]


def _find_difference2(piece: Piece, new_piece: Piece):
    'Takes the type of piece and orientation (e.g. T0) of two pieces and returns their difference in x and y coordinates'
    # FIXME: Hacky fix, might not work
    if piece.type == "O":
        # If piece is an O-piece, make the orientation 0 because all orientations are the same
        # (for the purpose of this function)
        piece.update(f'{piece.type}0{str(piece.x)}{str(piece.y)}')
        new_piece.update(
            f'{new_piece.type}0{str(new_piece.x)}{str(new_piece.y)}')
    x, y = _findBLC(piece)
    x2, y2 = _findBLC(new_piece)
    return x2 - x, y2 - y


def _find_kick_table(old_piece: Piece, new_piece: Piece):
    'Given a old piece and a new piece, returns the appropriate kick table'
    # Table for 180 kicks (from tetr.io) if difference in orientation is 2 or -2
    if old_piece.orientation - new_piece.orientation in [2, -2]:
        return storage.flip_table
    # Table for I piece kicks
    elif new_piece.type == "I":
        return storage.i_table
    else:
        # Table for JLSZT piece kicks
        assert new_piece.type in "JLSZT"
        return storage.jlszt_table


def _get_coord_from_kick(x_or_y, kick_tuple):
    'Given a string "x" or "y" and a kick tuple (e.g.) (0, -1), return the corresponding coordinate'
    if x_or_y == "x":
        # Tup is "(0, -1)" and [1:-1].split(", ") makes it into [0, -1] which is the x and y offsets
        return int(kick_tuple[1:-1].split(", ")[0])
    elif x_or_y == "y":
        return int(kick_tuple[1:-1].split(", ")[1])
    else:
        raise ValueError(f"Bad argument, x_or_y is '{x_or_y}'")


def _generate_coords_list(new_piece: Piece, table):
    'Given a piece and a kick table, generate all coordinates of the new piece with kick offsets applied'
    # Get_coord_from table gets the x and y coordinates from the tuple
    return [(int(new_piece.x) + _get_coord_from_kick("x", tup), int(new_piece.y) + _get_coord_from_kick("y", tup)) for tup in table]


def _check_kick_tables(old_piece_notation, new_piece_notation, board_notation):
    '''Takes a piece notation, board notation, direction and returns the piece notation
    after checking kicktables, or False if rotation is impossible. Also returns the number
    of the kick that was used, or False if rotation is impossible'''
    # Create new Pieces for future reference
    old_piece = Piece(old_piece_notation)
    new_piece = Piece(new_piece_notation)
    # If the piece is O, the rotation will always work, so return the new piece notation
    if new_piece.type == "O":
        return new_piece_notation, 0
    # First, check the original notation if it works
    b = update_boardstate(board_notation, new_piece)
    if b not in ["out of bounds", "occupied cell"]:
        # If there is no problem, return immediately
        return new_piece_notation, 0
    # If it doesn't work, check the kicks
    # Gets a message for the directions that will be looked up later
    direction_message = str(old_piece.orientation) + str(new_piece.orientation)
    # Finds the corresponding kick table
    table = _find_kick_table(old_piece, new_piece)[direction_message]
    # Generate a list with the new coordinates, offsetted with each of the kicks
    # [1:] is to remove first kick (0, 0) that has already been checked
    coords_list = _generate_coords_list(new_piece, table)[1:]
    # Uses a kick_counter (via enumerate) to keep track of which kick this is on (starts on 1st kick)
    for kick_counter, (new_x, new_y) in enumerate(coords_list, start=1):
        # Generate a piece message with the new orientation, and x and y values
        new_piece_message = new_piece.type + \
            str(new_piece.orientation) + str(new_x) + str(new_y)
        b = update_boardstate(board_notation, Piece(new_piece_message))
        if b not in ["out of bounds", "occupied cell"]:
            return new_piece_message, kick_counter
    # This means all kicks have been checked, and none work
    # Return false, meaning rotation is impossible
    return False, False


def _find_rotation_factor(rotation_direction):
    'Given a rotation direction (text), returns the rotation factor associated with that.'
    # Converts the rotation direction into a number used later
    if rotation_direction == "CW":
        return 1
    elif rotation_direction == "CCW":
        return 3
    elif rotation_direction == "180":
        return 2
    else:
        raise ValueError(f"Bad rotation_direction: '{rotation_direction}'")


def _find_rotation_direction(rotation_factor: int):
    'Given a rotation factor, returns the rotation direction (text) associated with that.'
    if rotation_factor == 1:
        return "CW"
    elif rotation_factor == 3:
        return "CCW"
    elif rotation_factor == 2:
        return "180"
    else:
        raise ValueError(f"Bad rotation_factor: '{rotation_factor}'")


def _find_piece_message(piece: Piece, new_direction: int):
    'Takes a Piece and new direction, and returns the new piece message with updated x and y coordinates'
    new_piece = Piece(piece.type + str(new_direction) +
                      str(piece.x) + str(piece.y))
    # Finds the difference in the two shapes
    x_diff, y_diff = _find_difference2(piece, new_piece)
    # Finds the new x and y coordinates
    new_x, new_y = str(int(piece.x)+x_diff), str(int(piece.y)+y_diff)
    # Returns the new piece message
    return piece.type+str(new_direction)+new_x+new_y


def rotate_and_update(pb_notation, direction):
    '''Takes a piece-board notation and a direction of rotation, \n
    and returns a new piece-board notation with the current piece rotated'''
    piece_n, b = separate_piece_board_notation(pb_notation)
    piece_n = Piece(piece_n)
    rotation_factor = _find_rotation_factor(direction)
    # Finds the new direction based on the original direction and the rotation
    new_direction = (int(piece_n.orientation) + rotation_factor) % 4
    piece_message = _find_piece_message(piece_n, new_direction)
    final_piece_notation, kick_number = _check_kick_tables(
        piece_n.value, piece_message, b)
    # If the piece cannot be rotated (all kicks are checked or it is an O piece)
    if final_piece_notation == False:
        # Make the piece notation the original value
        final_piece_notation = piece_n.value
    return construct_piece_board_notation(final_piece_notation, b), kick_number


def add_ghost_piece_and_update(piece: Piece, boardstate):
    "Takes a Piece and a boardstate, and returns a boardstate with the two combined, with ghost pieces"
    output = boardstate
    if piece.y == 0:
        return update_boardstate(output, piece)
    # Start on y below current piece, check until 0 going downwards.
    for index in range(piece.y, -1, -1):
        # Combine piece and ghost piece, giving piece the overlaps
        coord_dict = _combine_coordlists(
            [piece, Piece(f"{piece.type.lower()}{piece.orientation}{piece.x}{index}")])
        # Try updating boardstate with this
        check = update_boardstate(boardstate, piece, coord_dict)
        if check in ["out of bounds", "occupied cell"]:
            break
            # return update_boardstate(boardstate, piece) if index + 1 == piece.y else update_boardstate(output, piece)
        else:
            output = check
    # if index == piece.y-1:
    #     return update_boardstate(output, piece)
    return output


def check_line_clears(b_notation):
    'Given a board notation, check whether there are any line clears, and return a tuple of (new board notation, number of lines cleared, which lines were cleared (a list of indices of the original board notation))'
    # Removes starting asterisk and turns it into a list of rows
    b_notation = b_notation[1:].split("/")
    # Makes a copy of board_notation for iteration
    b_notation_copy = list(b_notation)
    filled_rows = []
    for index, row in enumerate(b_notation_copy):
        # Checking for garbage rows first
        # TODO: Clarify
        # Skip empty rows
        if row == "":
            continue
        if row[0] == "g":
            if len(row) != 3 or row[2] == ".":
                # Skip the row
                continue
            # No empty spaces, meaning this is a filled row
            filled_rows.append(index)
            b_notation.remove(row)
        for cell in row:
            # Empty spaces, whether in a garbage row or a normal row
            if cell.isnumeric() == True:
                # Skip this row
                break
        else:
            # No empty spaces, meaning this is a filled row
            filled_rows.append(index)
            # If there are duplicate rows, will remove one of them (both will be removed anyway)
            b_notation.remove(row)
    # Return new board notation, number of rows cleared, which rows were cleared
    # TODO: Determine whether (which rows were cleared) will actually be used or should be removed
    return "*" + "/".join(b_notation), len(filled_rows), filled_rows


def _access_corners(p: Piece, b: str) -> List[bool]:
    'Given a t-Piece, and the board it is in, this accesses and returns the four corners around the center\nReturns True if there is something there and False if the cell is empty'
    center_x, center_y = _find_center(p)
    # Corner offsets (from center) in a clockwise direction from the top left
    offset_list = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
    output_list = []
    # Check each offset to see if it's filled
    for x_offset, y_offset in offset_list:
        new_x, new_y = center_x+x_offset, center_y+y_offset
        # If cell is a wall (considered filled)
        if new_x < 0 or new_x > 9 or new_y < 0:
            output_list.append(True)
        # If cell is empty
        elif access_cell(b, new_y, new_x) == ".":
            output_list.append(False)
        else:
            output_list.append(True)
    return output_list


def _check_corners(p: Piece, b: str):
    filled_list = _access_corners(p, b)
    orientation = p.orientation
    # Magic to access the front and back two corners (e.g. orientation 2, front = 2 and 3, back = 0 and 1)
    front_two_corners = [filled_list[orientation],
                         filled_list[(orientation+1) % 4]]
    back_two_corners = [
        filled_list[(orientation+2) % 4], filled_list[(orientation+3) % 4]]
    # Check if the front two corners are filled and at least one in the back in empty
    if front_two_corners == [True, True] and True in back_two_corners:
        return "t-spin"
    elif True in front_two_corners and back_two_corners == [True, True]:
        return "t-spin mini"
    else:
        return False


def check_t_spin(pb_notation, replay_notation, last_kick_number):
    'Given a piece-board notation and replay notation, return whether this was a t-spin ("t-spin"), t-spin mini ("t-spin mini"), or not a t-spin (False)'
    p, b = separate_piece_board_notation(pb_notation)
    p = Piece(p)
    # Verifies that the piece is a t-piece and that the last movement was a rotation
    # replay notation.split("\n")[-1] will be {action} {delay}, so finds the action
    if p.type != "T" or replay_notation.split("\n")[-1].split(" ")[0] not in {'CW', 'CCW', '180'}:
        return False
    message = _check_corners(p, b)
    # Message will be t-spin, t-spin mini, or False
    if message == "t-spin mini" and last_kick_number == 4:
        # If the last kick is 4, this is a t-spin, not a t-spin mini (e.g. STSD)
        return "t-spin"
    return message
