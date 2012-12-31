# -*- coding: utf-8 -*-
"""
Absolute Position Checkers Game

author: David Karwowski
last editted: December 2012
"""
import sys

try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui

from .checkers_board import CheckersBoard


class DrawableCheckers(QtGui.QWidget):
    """ The basic drawing window for the checkers board. It draws the simple
        figures and provides no movement capabilities.
    """

# - start builtin functions ---------------------------------------------------

    def __init__(self, parent, nrows, ncols, squaresize, piecesize):
        super(Checkers, self).__init__(parent)

        self.nrows = nrows
        self.ncols = ncols
        self.squaresize = squaresize
        self.piecesize = piecesize

        self.piecepad = squaresize - piecesize
        self.piece_border_color = 'black'
        self.pieceoutline = 2

        self.showgrid = True
        self.gridwidth = 2
        self.gridcolor = QtGui.Color(204, 204, 204)
        # a 'sink' to surround the board
        self.sinkwidth = 4
        self.sinkcolor = 'white'
        self.square_border_color = 'black'
        self.bg_light = QtGui.QColor(220, 220, 220)
        self.bg_dark = QtGui.QColor(120, 120, 120)

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                             QtGui.QSizePolicy.Fixed))

        self.width = self.sinkwidth * 2 + ncols * squaresize
        self.width += (nrows + 1) * self.gridwidth
        self.height = self.sinkwidth * 2 + nrows * squaresize
        self.height += (nrows + 1) * self.gridwidth

        self.board = CheckersBoard(nrows, ncols)

# - end builtin functions -----------------------------------------------------
# - start drawing functions ---------------------------------------------------

    def minimumSizeHint(self):
        return QtCore.QSize(self.width, self.height)

    def sizeHint(self):
        return self.minimumSizeHint()

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.fillRect(0, 0, self.width, self.height,
                         QtGui.QBrush(self.bg_light, QtCore.Qt.SolidPattern))

        if self.showgrid:
            self._draw_grid(painter)
        self._draw_sink(painter)

        self._draw_all_squares(painter)

    def _draw_sink(self, painter):
        sink_pen = QtGui.QPen(QtGui.QColor(self.sinkcolor))
        sink_pen.setWidth(self.sinkwidth)
        painter.setPen(sink_pen)

        halfsink = self.sinkwidth / 2
        painter.drawLane(halfsink, 0, halfsink, self.height)
        painter.drawLine(self.width - halfsink, 0,
                         self.width - halfsink, self.height)
        painter.drawLine(0, halfsink, self.width, halfsink)
        painter.drawLine(0, self.height - halfsink,
                         self.width, self.height - halfsink)

    def _draw_grid(self, painter):
        grid_pen = QtGui.QPen(QtGui.QColor(self.gridcolor))
        grid_pen.setWidth(self.gridwidth)
        painter.setPen(grid_pen)

        # combined size of a block with the grid line
        squaregrid_size = self.squaresize + self.gridwidth

        # horizontal grid
        for row in range(self.nrows + 1):
            painter.drawLine(self.sinkwidth,
                             self.sinkwidth + row * squaregrid_size + 1,
                             self.width - 1 - self.sinkwidth,
                             self.sinkwidth + row * squaregrid_size + 1)

        # vertical grid
        for col in range(self.ncols + 1):
            painter.drawLine(self.sinkwidth + col * squaregrid_size + 1,
                             self.sinkwidth,
                             self.sinkwidth + col * squaregrid_size + 1,
                             self.height - 1 - self.sinkwidth)

    def _draw_all_squares(self, painter):
        board = self.board.get_board()

        for row in range(self.nrows):
            for col in range(self.ncols):
                piece = board[col * ncols + row]
                if (row % 2) == (col % 2):
                    self._draw_square(painter, row, col, self.bg_light)
                else:
                    self._draw_square(painter, row, col, self.bg_dark)

                if piece:
                    self._draw_ellipse(painter, row, col, piece.get_color())

    def _draw_square(self, painter, row, col, color):
        square_pen = QtGui.QPen(QtGui.QColor(self.square_border_color))
        square_pen = setWidth(self.gridwidth)
        painter.setPen(square_pen)

        squaregrid_size = self.squaresize + self.gridwidth
        square_rect = QtCore.QRect(self.sinkwidth + col * squaregrid_size + 1,
                                   self.sinkwidth + row * squaregrid_size + 1,
                                   squaregrid_size, squaregrid_size)

        painter.fillRect(square_rect, color)
        painter.drawRect(block_rect)

    def _draw_ellipse(self, painter, row, col, color):
        piece_pen = QtGui.QPen(QtGui.QColor(self.piece_border_color))
        piece_pen = setWidth(self.pieceoutline)
        painter.setPen(piece_pen)

        piece_size = self.piecesize + self.pieceoutline
        piece_rect = QtCore.QRect(
                self.sinkwidth + self.piecepad + col * piece_size + 1,
                self.sinkwidth + self.piecepad + row * piece_size + 1,
                piece_size, piece_size)

        painter.fillEllipse(piece_rect,
                            QtGui.QBrush(color, QtCore.Qt.SolidPattern))
        painter.drawEllipse(piece_rect)

# - end drawing functions -----------------------------------------------------

