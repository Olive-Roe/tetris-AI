from storage import colours_dict


def create_grid(locked_positions=None):
    if locked_positions is None:
        locked_positions = {}
    grid = [["black" for _ in range(10)] for _ in range(40)]
    for row in range(len(grid)):
        for col in range(len(grid[1])):
            if (row, col) in locked_positions:
                c = locked_positions[(row, col)]
                grid[row][col] = c
    return grid


def _get_line_from_garbage_message(message):
    # allows for g0L meaning a garbage line with orange
    type_of_piece = message[2] if len(message) == 3 else "."
    # message[1] is the garbage_index (3 in g3)
    return f'{"x"*int(message[1])}{type_of_piece}{"x"*(9-int(message[1]))}'


def _get_message_from_garbage_line(line):
    'Gets the shortened message from a garbage line (e.g. g6 from xxxxxx.xxx, or g2L from xxLxxxxxxx'
    index = 0
    # Default piece type is ., which isn't shown
    piece_type = ""
    for i, cell in enumerate(line):
        if cell != "x":
            # Finds the non garbage cell
            index = i
            if cell != ".":
                # Sets the piece type to the contents of the cell
                piece_type = cell
            break
    return f"g{str(index)}{piece_type}"


def _get_message_from_normal_line(line):
    lineStr = ""
    counter = 0
    for c in line:
        if c == ".":
            counter += 1
        else:
            lineStr += str(counter) + c if counter != 0 else c
            counter = 0
    # Add the counter one last time if it is still not 0
    lineStr += str(counter) if counter != 0 else ""
    return lineStr


def boardstate_to_extended_boardstate(boardstate: str):
    if boardstate == "*":
        return '*' + ("........../"*40)[:-1]
    # Remove starting asterisk
    boardstate = boardstate[1:]
    outputList = []
    for line in boardstate.split("/"):
        if line == "":
            outputList.append("..........")
        elif line[0] == "g":
            outputList.append(_get_line_from_garbage_message(line))
        else:
            outputList.append("".join(
                ["." * int(character) if character.isnumeric() else character for character in line]))
    outputStr = "*" + "/".join(outputList)
    for _ in range(40 - len(outputStr.split("/"))):
        outputStr += "/.........."
    return outputStr


def extended_boardstate_to_boardstate(extended_boardstate: str):
    # TODO: Short-circuit this function to run faster even if there are more pieces
    if extended_boardstate == '*' + ("........../"*40)[:-1]:
        return "*"
    # Remove asterisk
    extended_boardstate = extended_boardstate[1:]
    outputList = []
    # Look at list in reverse order to remove unnecessary empty lines
    emptyRows = True
    for line in extended_boardstate.split("/")[::-1]:
        if line == "..........":
            if emptyRows:
                # Skip the empty row
                continue
            outputList.append("")
        else:
            emptyRows = False
            # The rows up until now are empty, now we have some non-empty rows
            if "x" in line:
                outputList.append(_get_message_from_garbage_line(line))
            else:
                outputList.append(_get_message_from_normal_line(line))
    # Un-reverse the list to get the correct order
    return "*" + "/".join(outputList[::-1])


def board_notation_to_dict(notation):
    notation = boardstate_to_extended_boardstate(notation)
    # Remove starting asterisk
    notation = notation[1:]
    output_list = []
    rows = len(notation.split("/"))
    for row in notation.split("/"):
        if row == "":
            output_list.extend("black" for _ in range(10))
        for index in range(len(row)):
            item = row[index]
            # Whether it's S or . check color dict and append the respective colour
            output_list.append(colours_dict[item])
    indices = [(x, y) for x in range(rows) for y in range(10)]
    try:
        items_list = [(indices[i], output_list[i]) for i in range(rows * 10)]
    # TODO: Add a more specific except here
    except:
        print(output_list)
        raise ValueError(
            f"Invalid board notation. Length of output_list: {len(output_list)}")
    return dict(items_list)


def type_of_boardstate(boardstate):
    if type(boardstate) == list:
        return "list form"
    return "extended boardstate" if "." in boardstate else "boardstate"


def boardstate_to_list_form(boardstate: str):
    'Returns a 2D array of cells inside rows from a boardstate'
    type_b = type_of_boardstate(boardstate)
    if type_b == "boardstate":
        # we need to extend the boardstate
        a = boardstate_to_extended_boardstate(boardstate)
    elif type_b == "extended boardstate":
        # boardstate is already extended, shorten it and extend it again
        # TODO: check whether this is necessary as it slows whole program down
        a = boardstate_to_extended_boardstate(
            extended_boardstate_to_boardstate(boardstate))

    # if neither of these an error will be thrown
    # Remove starting asterisk and split a
    a = a[1:].split("/")
    return [list(item) for item in a]  # output


def list_form_to_boardstate(list_form: list):
    return "*" + "/".join(["".join(item) for item in (list_form)])


def construct_piece_board_notation(piece_notation, board_notation):
    'Returns str of piece board notation'
    return f"{piece_notation}:{board_notation}"


def return_x_y(piece_notation):
    if piece_notation[2] == "-":  # handling negative x/y values and 2 digit x values
        x_loc = int(str(piece_notation[2]) + str(piece_notation[3]))
        y_loc = int(piece_notation[4:])
    else:
        x_loc = piece_notation[2]
        y_loc = int(piece_notation[3:])
    return str(x_loc), str(y_loc)


def access_cell(boardstate: str, row: int, column: int):
    'Given a boardstate, row, and column of a cell (starting from index 0), return the value of the cell in the boardstate.'
    b = boardstate_to_extended_boardstate(boardstate)
    # Removes starting asterisk
    return b[1:].split("/")[row][column]


def change_cell(boardstate: str, row: int, column: int, val: str):
    # sourcery skip: use-fstring-for-concatenation
    'Given a boardstate, row, column of a cell (starting from index 0), and a value, update the boardstate and return it.'
    row = row
    column = column
    new_boardstate = boardstate_to_list_form(boardstate)
    new_boardstate[row][column] = val
    return list_form_to_boardstate(new_boardstate)


def separate_piece_board_notation(pb_notation):
    'Returns a tuple (piece_notation, board_notation)'
    return (pb_notation.split(":")[0], pb_notation.split(":")[1])


def type_of_boardstate(boardstate):
    if type(boardstate) == list:
        return "list form"
    return "extended boardstate" if "." in boardstate else "boardstate"


def display_as_text(notation):
    notation = boardstate_to_extended_boardstate(notation)
    for row in (notation.split("/")):  # reverse list
        print(row)


def check_type_notation(notation):
    # sourcery skip: merge-else-if-into-elif, reintroduce-else, use-next
    'Takes a (valid) notation and returns its type, or False if it\'s unrecognizable.'
    n_list = list(notation)
    if ":" in n_list:
        return "piece-board notation"
    elif "*" in n_list:
        if "." in n_list:
            return "extended board notation"
        for item in n_list:
            if item.isnumeric() == True:
                return "board notation"
        return False
    elif len(n_list) > 13 and len(n_list) < 21:
        return "bag notation"
    else:
        return "piece_notation"
