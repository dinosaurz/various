#!//usr//bin//env python2


class Piece(object):
    PIECE_ID = 0
    def __init__(self, color):
        """The constructor for a piece object. Input the color as a string.
            color should be 'red' or 'black'."""
        self.id = Piece.PIECE_ID
        self.crowned = False
        self.color = color

        Piece.PIECE_ID += 1

    def __eq__(self, other):
        """Equality test based on color."""
        return self.is_red() == other.is_red()

    def __repr__(self):
        """Representation when called as a string."""
        if self.is_crowned():
            return "R" if self.is_red() else "B"
        return "r" if self.is_red() else "b"

    def crown(self):
        """Set the piece to be crowned as a King."""
        self.crowned = True

    def get_id(self):
        """Getter for the id of the given Piece."""
        return self.id

    def is_crowned(self):
        """Getter for the crowned setting."""
        return self.crowned

    def is_red(self):
        """Test for whether the piece is red or not."""
        return "red" == self.color

    def is_black(self):
        """Test for whether the piece is black or not."""
        return "black" == self.color


class Board(object):
    def __init__(self, squares=None, width=8, height=8):
        """Board constructor to initialize the original placement of the pieces."""
        self.width = width
        self.height = height

        if not squares:
            self.squares = dict((i, None) for i in range(self.width * self.height))

            # 0 begins as the top of the board, making it black
            for i in range(self.width * 3):
                row, col = i // self.width, i % self.width
                if row % 2 == 0 and not col % 2 == 0:
                    self.squares[i] = Piece("black")
                if not row % 2 == 0 and col % 2 == 0:
                    self.squares[i] = Piece("black")
            # red would be the bottom 3 rows
            for i in range(self.width * (self.height - 3), self.width * self.height):
                row, col = i // self.width, i % self.width
                if row % 2 == 0 and not col % 2 == 0:
                    self.squares[i] = Piece("red")
                if not row % 2 == 0 and col % 2 == 0:
                    self.squares[i] = Piece("red")

    def move(self, original_pos, new_pos):
        """Moving a piece from position with coordinates in tuple format. Return whether move succeeds."""
        orig_x, orig_y = original_pos
        new_x, new_y = new_pos

        orig_i = orig_y * self.width + orig_x
        new_i = new_y * self.width + new_x

        # ensure there is no vertical or horizontal movement
        if any([orig_x - new_x, orig_y - new_y]) == 0:
            return False

        if self.squares[orig_i] and not self.squares[new_i]:
            if not self.squares[orig_i].is_crowned():
                if not self.squares[orig_i].is_red() and new_y < orig_y:
                    return False
                if not self.squares[orig_i].is_black() and new_y > orig_y:
                    return False
            self.squares[new_i], self.squares[orig_i] = self.squares[orig_i], None

        return True

    def jump(self, jumping_orig, jumping_over, jumping_land):
        """Test whether a jump is possible first, then try moving. Return whether jump succeeds."""
        orig_x, orig_y = jumping_orig
        over_x, over_y = jumping_over
        land_x, land_y = jumping_land

        orig_i = orig_y * self.width + orig_x
        over_i = over_y * self.width + over_x
        land_i = land_y * self.width + land_x

        # first two spots should exist, while the last one should return None
        if all([self.squares[orig_i], self.squares[over_i], not self.squares[land_i]]):
            # Ensure the two pieces are of different colors
            if not self.squares[orig_i] == self.squares[over_i]:
                if self.move(jumping_orig, jumping_land):
                    self.squares[over_i] = None
                    return True
        return False

    def crown(self, piece):
        """Enhance the piece to be able to move in reverse as well."""
        piece_x, piece_y = piece
        piece_i = piece_y * self.width + piece_x

        # Ensure the piece is in the last column from the starting position
        if piece_y == self.height - 1 and self.squares[piece_i].is_black():
            self.squares[piece_i].crown()
        elif piece_y == 0 and self.squares[piece_i].is_red():
            self.squares[piece_i].crown()
        else:
            return False
        return True

