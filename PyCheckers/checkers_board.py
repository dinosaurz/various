# -*- coding: utf-8 -*-
"""
Board implementation of the checkers game

author: David Karwowski
editted: December 2012
"""

class Piece(object):
    PIECE_ID = 0

# - start basic functions -----------------------------------------------------

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

    def __ne__(self, other):
        """Equality test based on the color."""
        return not self.__eq__(other)

    def __repr__(self):
        """Representation when called as a string."""
        if self.is_crowned():
            return "R" if self.is_red() else "B"
        return "r" if self.is_red() else "b"

# - end basic functions -------------------------------------------------------
# - start misc. functions -----------------------------------------------------

    def crown(self):
        """Set the piece to be crowned as a King."""
        self.crowned = True

    def get_id(self):
        """Getter for the id of the given Piece."""
        return self.id

# - end misc. functions -------------------------------------------------------
# - start boolean functions ---------------------------------------------------

    def is_crowned(self):
        """Getter for the crowned setting."""
        return self.crowned

    def is_red(self):
        """Test for whether the piece is red or not."""
        return "red" == self.color

    def is_black(self):
        """Test for whether the piece is black or not."""
        return "black" == self.color

    def can_move(self, p_pos, o_pos):
        """Test whether the piece is capable of moving.
        Attributes
            p_pos : (x, y)
            o_pos : ( (x, y), Piece ) [1 .. 4]
        """
        pos_x, pos_y = p_pos

        possibles = [other[0] for other in o_pos if not other[1]]
        if self.is_black() and not self.is_crowned():
            moves = [m for m in possibles if m[1] > pos_y]  # limit forward
        elif self.is_red() and not self.is_crowned():
            moves = [m for m in possibles if m[1] < pos_y]  # limit forward
        elif self.is_crowned():
            moves = [m for m in possibles]  # no limits on movement necessary
        else:
            moves = [] # how the fuck did the color not get set right?

        return moves if moves else None

    def can_jump(self, orig_pos, over_pos, land_pos):
        """Test whether the piece is capable of completing the given jumps.
        Attributes
            orig_pos : (x, y)
            over_pos : ( (x, y), Piece ) [1 .. 4]
            land_pos : ( (x, y), Piece ) [1 .. 4]
        """
        possibles = []
        # test the possible jumps first
        for i, _ in enumerate(over_pos):  # same length as land_pos
            if over_pos[i][1] and self != over_pos[i][1]:
                possibles.append(land_pos[i])
        return self.can_move(orig_pos, possibles)

# - end boolean functions -----------------------------------------------------


class CheckersBoard(object):

# - start builtin functions ---------------------------------------------------

    def __init__(self, squares=None, ncols=8, nrows=8):
        """Board constructor to initialize the placement of the pieces."""
        self.ncols = ncols
        self.nrows = nrows

        if not squares:
            self.squares = dict((i, None) for i in xrange(ncols * nrows))

            # 0 begins as the top of the board, making it black
            for i in xrange(ncols * 3):
                row, col = i // ncols, i % ncols
                if row % 2 == col % 2:
                    self.squares[i] = Piece("black")
            # red would be the bottom 3 rows
            for i in xrange(ncols * (nrows - 3), ncols * nrows):
                row, col = i // ncols, i % ncols
                if row % 2 == col % 2:
                    self.squares[i] = Piece("red")

    # testing purpose drawing of the board
    def __repr__(self):
        """Way to represent the board itself through an ascii display."""
        ncols, nrows = self.ncols, self.nrows  # easier to read

        rep = " ".join([str(n-1) if n else " " for n in xrange(self.ncols+1)])
        for piece in self.squares:
            if piece in [i for i in xrange(0, ncols * nrows, ncols)]:
                rep += "\n{0} ".format(piece // ncols)

            if self.squares[piece]:
                rep += "{0} ".format(self.squares[piece])
            else:
                rep += "- "

        return rep

# - end builtin functions -----------------------------------------------------
# - start piece movement functions --------------------------------------------

    def move(self, orig_pos, new_pos):
        """Movement function to push the piece through the positions."""
        orig_x, orig_y = orig_pos
        new_x, new_y = new_pos

        orig_i = orig_y * self.ncols + orig_x
        new_i = new_y * self.ncols + new_x

        orig_piece = self.squares[orig_i]
        new_piece = self.squares[new_i]

        # ensure there is no vertical or horizontal movement
        if orig_piece.can_move(orig_pos, [(new_pos, new_piece)]):
            self.squares[new_i] = self.squares[orig_i]
            self.squares[orig_i] = None
            return True
        return False

    def jump(self, j_orig, j_over, j_land):
        """Movement function to jump one piece over another."""
        orig_x, orig_y = j_orig
        over_x, over_y = j_over
        land_x, land_y = j_land

        # indexes for each square
        orig_i = orig_y * self.ncols + orig_x
        over_i = over_y * self.ncols + over_x
        land_i = land_y * self.ncols + land_x

        # piece for quicker access
        orig_p = self.squares[orig_i]
        over_p = self.squares[over_i]
        land_p = self.squares[land_i]

        if orig_p.can_jump(j_orig, [(j_over, over_p)], [(j_land, land_p)]):
            self.squares[land_i] = self.squares[orig_i]
            self.squares[over_i], self.squares[orig_i] = None, None
            return True
        return False

    def crown(self, piece):
        """Enhance the piece to be able to move in reverse as well."""
        piece_x, piece_y = piece
        piece_i = piece_y * self.ncols + piece_x

        # Ensure the piece is in the last column from the starting position
        if piece_y == self.nrows - 1 and self.squares[piece_i].is_black():
            self.squares[piece_i].crown()
        elif piece_y == 0 and self.squares[piece_i].is_red():
            self.squares[piece_i].crown()
        else:
            return False
        return True

# - end piece movement functions ----------------------------------------------
# - start possible movement functions -----------------------------------------

    def possible_moves(self, piece):
        """Return a list of coordinated in (x, y) format for possible landing.
        Attributes
            piece : (x, y)
        """
        def _index(orig, off):
            """Helper function to find the new index."""
            orig_x, orig_y = orig
            off_x, off_y = off
            return (orig_y - off_y) * self.ncols + (orig_x - off_x)

        p_x, p_y = piece
        p_i = _index(piece, (0, 0))

        # pass a list of the four corners first for basic possibles
        move_land = [((p_x + i, p_y + j), self.squares[_index(piece, (i, j))])\
                     for i in [-1, 1] for j in [-1, 1]]
        possibles = self.squares[p_i].can_move(piece, move_land)

        # next append the new list from jumps
        jump_land = [((p_x + i, p_y + j), self.squares[_index(piece, (i, j))])\
                     for j in [-2, 2] for i in [-2, 2]]
        possibles += self.squares[p_i].can_jump(piece, move_land, jump_land)

        # clean out the list of duplicates, although there should be none
        return [m for i, m in enumerate(possibles) if m not in possibles[:i]]

# - end possible movement functions -------------------------------------------
# - start boolean functions ---------------------------------------------------

    def red_has_won(self):
        """Test is red has won or not."""
        return not any([self.squares[p].is_red() for p in self.squares        \
                        if self.squares[p]])

    def black_has_won(self):
        """Test whether black has won or not."""
        return not any([self.squares[p].is_black() for p in self.squares      \
                        if self.squares[p]])

# - end boolean functions -----------------------------------------------------
# - start getter functions ----------------------------------------------------

    def get_piece(self, index):
        """Get the necessary piece at the index given."""
        return self.squares[index]

    def get_ncols(self):
        """Return the ncols of the board."""
        return self.ncols

    def get_nrows(self):
        """Return the nrows of the board."""
        return self.nrows

    def get_board(self):
        """Return the entire board if necessary."""
        return self.squares

