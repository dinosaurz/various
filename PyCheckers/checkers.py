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

        # selection information
        self.select_col = None
        self.select_row = None
        self.first_selected = False
        self.first_col = None
        self.first_row = None
        self.select_border_color = 'white'
        self.select_outline = 2

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
        self._draw_selections(painter)

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

        # combined size of a square with the grid line
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
        painter.drawRect(square_rect)

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

    def _draw_selection(self, painter):
        select_pen = QtGui.QPen(QtGui.QColor(self.select_border_color))
        select_pen.setWidth(self.select_outline)
        painter.setPen(select_pen)

        select_size = self.piecesize + self.select_outline
        select_rect = None
        col, row = select_col, select_row

        if row and col:
            select_rect = QtCore.QRect(self.sinkwidth + col * select_size + 1,
                                       self.sinkwidth + row * select_size + 1,
                                       select_size, select_size)
        elif row:
            select_rect = QtCore.QRect(self.sinkwidth + 1,
                                       self.sinkwidth + row * select_size + 1,
                                       select_size, select_size * self.ncols)
        elif col:
            select_rect = QtCore.QRect(self.sinkwidth + col * select_size + 1,
                                       self.sinkwidth + 1,
                                       select_size * self.nrows, select_size)
        else:
            return

        self.drawRect(select_rect)

    def _clear_selections(self):
        if self.select_row or self.select_col:
            self.select_row = None
            self.select_col = None
        else:
            self.first_selected = False
            self.first_col = None
            self.first_row = None

    def _enter_selections(self):
        self._clear_selections()
        if not all([self.select_col, self.select_row]):
            return

        if self.first_selected:
            orig = (self.first_col, self.first_row)
            land = (self.select_col, self.select_row)
            if self.select_row - self.first_row == 2:
                over = (self.select_col - self.first_col,
                        self.select_row - self.select_col)
                self.board.jump(orig, over, land)
            else:
                self.board.jump(orig, land)
        else:
            self.first_selected = True
            self.first_col = self.select_col
            self.first_row = self.select_row

    def _select_col(self, col):
        self.select_col = col

    def _select_row(self, row):
        self.select_row = row

# - end drawing functions -----------------------------------------------------


class MainCheckers(DrawableCheckers):
    """ The main checkers window, with pieces that can be moved through
        clicking on the piece and selecting a legal move to change to.
        Added support will create a "Legal move" feature to highlight
        choices of landings.
    """
    def __init__(self, parent, nrows, ncols, squaresize):
        super(MainCheckers, self).__init__(parent, nrows, ncols, squaresize)

        # Dictionary to decide what to do based on key presses
        self.general_keys = {QtCore.Qt.Key_Escape: self._clear_selections,
                             QtCore.Qt.Key_Enter:  self._enter_selections}
        self.col_keys = {QtCore.Qt.Key_A: 0, QtCore.Qt.Key_B: 1,
                         QtCore.Qt.Key_C: 2, QtCore.Qt.Key_D: 3,
                         QtCore.Qt.Key_E: 4, QtCore.Qt.Key_F: 5,
                         QtCore.Qt.Key_G: 6, QtCore.Qt.Key_H: 7}
        self.row_keys = {QtCore.Qt.Key_1: 0, QtCore.Qt.Key_2: 1,
                         QtCore.Qt.Key_3: 2, QtCore.Qt.Key_4: 3,
                         QtCore.Qt.Key_5: 4, QtCore.Qt.Key_6: 5,
                         QtCore.Qt.Key_7: 6, QtCore.Qt.Key_8: 7}

# - start control functions ---------------------------------------------------

    def restart(self):
        self.board = CheckersBoard(self.nrows, self.ncols)
        self.update()

    def keyPressEvent(self, event):
        if event.key() in self.general_keys:
            self.general_keys[event.key()]()
        elif event.key() in self.col_keys:
            self._select_col(self.col_keys[event.key()])
        elif event.key() in self.row_keys:
            self._select_row(self.row_keys[event.key()])
        else:
            return

        self.update()

    def mousePressEvent(self, event):
        col = event.x() // self.width
        row = event.y() // self.height

        self._select_col(col)
        self._select_row(row)

        self.update()

