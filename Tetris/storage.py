# Kick table for jlszt pieces
jlszt_table = {'01': ['(0, 0)', '(-1, 0)', '(-1, 1)', '(0, -2)', '(-1, -2)'], '10': ['(0, 0)', '(1, 0)', '(1, -1)', '(0, 2)', '(1, 2)'], '12': ['(0, 0)', '(1, 0)', '(1, -1)', '(0, 2)', '(1, 2)'], '21': ['(0, 0)', '(-1, 0)', '(-1, 1)', '(0, -2)', '(-1, -2)'], '23': ['(0, 0)', '(1, 0)', '(1, 1)', '(0, -2)', '(1, -2)'], '32': ['(0, 0)', '(-1, 0)', '(-1, -1)', '(0, 2)', '(-1, 2)'], '30': ['(0, 0)', '(-1, 0)', '(-1, -1)', '(0, 2)', '(-1, 2)'], '03': ['(0, 0)', '(1, 0)', '(1, 1)', '(0, -2)', '(1, -2)']}
# Kick table for i pieces
i_table = {'01': ['(0, 0)', '(-2, 0)', '(1, 0)', '(-2, -1)', '(1, 2)'], '10': ['(0, 0)', '(2, 0)', '(-1, 0)', '(2, 1)', '(-1, -2)'], '12': ['(0, 0)', '(-1, 0)', '(2, 0)', '(-1, 2)', '(2, -1)'], '21': ['(0, 0)', '(1, 0)', '(-2, 0)', '(1, -2)', '(-2, 1)'], '23': ['(0, 0)', '(2, 0)', '(-1, 0)', '(2, 1)', '(-1, -2)'],'32': ['(0, 0)', '(-2, 0)', '(1, 0)', '(-2, -1)', '(1, 2)'], '30': ['(0, 0)', '(1, 0)', '(-2, 0)', '(1, -2)', '(-2, 1)'], '03': ['(0, 0)', '(-1, 0)', '(2, 0)', '(-1, 2)', '(2, -1)']}
# Kick table for 180 degree rotations
flip_table = {'02': ['(0, 0)', '(0, 1)', '(1, 1)', '(-1, 1)', '(1, 0)', '(-1, 0)'], '20': ['(0, 0)', '(0, -1)', '(1, -1)', '(-1, 0)', '(-1, 0)', '(1, 0)'], '13': ['(0, 0)', '(1, 0)', '(1, 2)', '(1, 1)', '(0, 2)', '(0, 1)'], '31': ['(0, 0)', '(-1, 0)', '(-1, 2)', '(-1, 1)', '(0, 2)', '(0, 1)']}

# Different pieces and what they look like
pieces = {'I': [['.....', '0000.', '.....', '.....', '.....'], ['.0...', '.0...', '.0...', '.0...', '.....'], ['.....', '.....', '0000.', '.....', '.....'], ['..0..', '..0..', '..0..', '..0..', '.....']], 'J': [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']], 'L': [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']], 'O': [['.....', '.....', '.00..', '.00..', '.....']], 'S': [['.....', '..00..', '.00...', '......', '.....'], ['.....', '..0..', '..00.', '...0.', '.....'], ['.....', '......', '..00..', '.00...', '.....'], ['.....', '.0...', '.00..', '..0..', '.....']], 'Z': [['.....', '.00..', '..00.', '.....', '.....'], ['.....', '...0.', '..00.', '..0..', '.....'], ['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']], 'T': [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]}

# Table for the bottom left corner of the different shapes
blc_table = {"I": [(0, 3), (1, 1), (0, 2), (2, 1)],
       "J": [(1, 2), (2, 1), (3, 1), (1, 1)],
       "L": [(1, 2), (2, 1), (1, 1), (2, 1)],
       "O": [(1, 1), (1, 1), (1, 1), (1, 1)],
       "S": [(1, 2), (2, 1), (1, 1), (3, 1)],
       "Z": [(2, 2), (2, 1), (2, 1), (1, 1)],
       "T": [(1, 2), (2, 1), (2, 1), (2, 1)]}

# Table for the list of offsets from the center of the different shapes
offset_list_table = {'I': [[(-2, 1), (-1, 1), (0, 1), (1, 1)], [(-1, 2), (-1, 1), (-1, 0), (-1, -1)], [(-2, 0), (-1, 0), (0, 0), (1, 0)], [(0, 2), (0, 1), (0, 0), (0, -1)]], 'J': [[(-1, 1), (-1, 0), (0, 0), (1, 0)], [(0, 1), (1, 1), (0, 0), (0, -1)], [(-1, 0), (0, 0), (1, 0), (1, -1)], [(0, 1), (0, 0), (-1, -1), (0, -1)]], 'L': [[(1, 1), (-1, 0), (0, 0), (1, 0)], [(0, 1), (0, 0), (0, -1), (1, -1)], [(-1, 0), (0, 0), (1, 0), (-1, -1)], [(-1, 1), (0, 1), (0, 0), (0, -1)]], 'O': [[(-1, 0), (0, 0), (-1, -1), (0, -1)], [(-1, 0), (0, 0), (-1, -1), (0, -1)], [(-1, 0), (0, 0), (-1, -1), (0, -1)], [(-1, 0), (0, 0), (-1, -1), (0, -1)]], 'S': [[(0, 1), (1, 1), (-1, 0), (0, 0)], [(0, 1), (0, 0), (1, 0), (1, -1)], [(0, 0), (1, 0), (-1, -1), (0, -1)], [(-1, 1), (-1, 0), (0, 0), (0, -1)]], 'Z': [[(-1, 1), (0, 1), (0, 0), (1, 0)], [(1, 1), (0, 0), (1, 0), (0, -1)], [(-1, 0), (0, 0), (0, -1), (1, -1)], [(0, 1), (-1, 0), (0, 0), (-1, -1)]], 'T': [[(0, 1), (-1, 0), (0, 0), (1, 0)], [(0, 1), (0, 0), (1, 0), (0, -1)], [(-1, 0), (0, 0), (1, 0), (0, -1)], [(0, 1), (-1, 0), (0, 0), (0, -1)]]}

# Table for the list of offsets from the BLC
blc_offsets = {'I': [[(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 3), (0, 2), (0, 1), (0, 0)], [(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 3), (0, 2), (0, 1), (0, 0)]], 'J': [[(0, 1), (0, 0), (1, 0), (2, 0)], [(0, 2), (1, 2), (0, 1), (0, 0)], [(-2, 1), (-1, 1), (0, 1), (0, 0)], [(1, 2), (1, 1), (0, 0), (1, 0)]], 'L': [[(2, 1), (0, 0), (1, 0), (2, 0)], [(0, 2), (0, 1), (0, 0), (1, 0)], [(0, 1), (1, 1), (2, 1), (0, 0)], [(-1, 2), (0, 2), (0, 1), (0, 0)]], 'O': [[(0, 1), (1, 1), (0, 0), (1, 0)], [(0, 1), (1, 1), (0, 0), (1, 0)], [(0, 1), (1, 1), (0, 0), (1, 0)], [(0, 1), (1, 1), (0, 0), (1, 0)]], 'S': [[(1, 1), (2, 1), (0, 0), (1, 0)], [(0, 2), (0, 1), (1, 1), (1, 0)], [(1, 1), (2, 1), (0, 0), (1, 0)], [(-2, 2), (-2, 1), (-1, 1), (-1, 0)]], 'Z': [[(-1, 1), (0, 1), (0, 0), (1, 0)], [(1, 2), (0, 1), (1, 1), (0, 0)], [(-1, 1), (0, 1), (0, 0), (1, 0)], [(1, 2), (0, 1), (1, 1), (0, 0)]], 'T': [[(1, 1), (0, 0), (1, 0), (2, 0)], [(0, 2), (0, 1), (1, 1), (0, 0)], [(-1, 1), (0, 1), (1, 1), (0, 0)], [(0, 2), (-1, 1), (0, 1), (0, 0)]]}

# Dictionary for what symbols correspond to what colors (turtle)
#TODO: Make transparent colors for ghost pieces (see if rgba can be implemented)
colours_dict = {
    "I": "cyan",
    "J": "blue",
    "L": "orange",
    "O": "yellow",
    "S": "lime",
    "Z": "red",
    "T": "magenta",
    ".": "black",
    "x": "grey",
    "i": "teal",
    "j": "navy",
    "l": "dark orange",
    "o": "olive",
    "s": "green",
    "z": "maroon",
    "t": "purple",
}


tetrio_atk = {
    "0": 0,
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 4,
}

tetrio_tspin_mini = {
    "0": 0,
    "1": 0,
    "2": 1,
}

tetrio_tspin = {
    "0": 0,
    "1": 2,
    "2": 4,
    "3": 6,
    "4": 10 # no idea how tspin quad is possible
}