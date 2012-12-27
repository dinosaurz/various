#!//usr//bin//env python2


class Piece(object):
    PIECE_ID = 0
    def __init__(self, color):
        """The constructor for a piece object. Input the color as a string.
            color should be 'red' or 'black'."""
        self.id = PIECE_ID
        self.crowned = False
        self.color = color

        Piece.PIECE_ID += 1

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

            # 0 begins as the bottom of the board, making it red
            for i in range(self.width * 3):
                if i % 2 == 0:
                    self.squares[i] = Piece("red")
            # black is the top 3 rows
            for i in range(self.width * (self.height - 3), self.width * self.height):
                if i % 2 == 0:
                    self.squares[i] = Piece("black")

    def move(self, original_pos, new_pos):
        """Moving a piece from position with coordinates in tuple format."""
        orig_x, orig_y = original_pos
        orig_place = orig_y * self.width + orig_x
        new_x, new_y = new_pos
        new_place = new_y * self.width + new_x

        if self.squares[orig_place] and not self.squares[new_place]
            if not self.squares[orig_place].is_crowned():
                if not self.squares[orig_place].is_red() and new_x < orig_x:
                    return
                if not self.squares[orig_place].is_black() and new_x > orig_x:
                    return
            self.squares[new_place], self.squares[orig_place] = self.squares[orig_place], None

    def jump(self, jumping_pos, jumping_ovr, jumping_new):

