#!/usr/bin/env python2
"""
Implementation of a checkers game written in Python 2.7.3
"""

# Globals for settings
# Directions to move
NW, NE, SW, SE = 0, 1, 2, 3
KING, REG, OFF = 0, 1, 2


class Position(object):
    """Keep the current location on the board"""
    def __init__(self, startx=0, starty=0):
        """Create new location on the board"""
        self.prev = []
        self.x = startx
        self.y = starty

    def move(self, direction):
        """Move the object in relation to the direction"""
        self.prev.append((self.x, self.y))
        self.x = (self.x - 1) if (direction % 2 == 0) else (self.x + 1)
        self.y = (self.y - 1) if (direction > 1) else (self.y + 1)

    def set_x(self, newx):
        """Directly setting the x value"""
        self.x = newx

    def set_y(self, newy):
        """Directly setting the y value"""
        self.y = newy

    def get_x(self):
        """Return the current x value"""
        return self.x

    def get_y(self):
        """Return the current y value"""
        return self.y


class Board(object):
    """Keep track of all pieces on the board"""
    def __init__(self, width, height):
        """Create the new board with no pieces"""
        self.height = height
        self.width = width
        self.black = {}
        self.red = {}

    def add_piece(self, ident, position, color, piece=REG):
        """Add a piece onto the board"""
        if color == "red":
            self.red[ident] = self.red.get(ident, (piece, position))
        elif color == "black":
            self.black[ident] = self.black.get(ident, (piece, position))
        else:
            raise KeyError

    def remove_piece(self, ident, color):
        """Take the piece off of the board"""
        if color == "red" and ident in self.red:
            self.red[ident] = (OFF, Position(-1, -1))
        elif color == "black" and ident in self.black:
            self.black[ident] = (OFF, Position(-1, -1))
        else:
            raise KeyError

