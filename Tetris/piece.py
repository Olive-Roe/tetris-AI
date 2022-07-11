from board_processing import return_x_y


class Piece:
    def __init__(self, piece_notation: str = ""):
        self.value = piece_notation
        self.x, self.y = return_x_y(piece_notation)
        self.x, self.y = int(self.x), int(self.y)
        self.type = piece_notation[0]
        self.orientation = int(piece_notation[1])

    def update(self, new_piece: str):
        self.value = new_piece
        self.x, self.y = return_x_y(new_piece)
        self.x, self.y = int(self.x), int(self.y)
        self.type = new_piece[0]
        self.orientation = int(new_piece[1])
