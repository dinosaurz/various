#!/usr/bin/env python2
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


class Checkers(QtGui.QWidget):

# - start builtin functions ---------------------------------------------------

    def __init__(self):
        super(Checkers, self).__init__()

        # Objects necessary
        self.board = Board()

        self._init_ui()

    def _init_ui(self):
        """Initialize all features in the UI itself."""
        # basic sizes for everything
        self.square_size, self.piece_size, self.pad = 50, 40, 20
        self.board_height = self.square_size * self.board.get_height()
        self.board_width = self.square_size * self.board.get_width()
        self.ui_height = self.board_height + 2 * self.pad
        self.ui_width = self.board_width + 2 * self.pad

        # create the inner board
        self.ui_board = QtGui.QFrame(self)
        self.ui_board.setGeometry(self.pad, self.pad,                         \
                                  self.board_width, self.board_height)
        self.ui_board.setStyleSheet("QWidget { background-color: black }")

        # True UI creation
        self.setGeometry(200, 200, self.ui_width, self.ui_height)
        self.setWindowTitle("Checkers v0.1")
        self.show()

# - end builtin functions -----------------------------------------------------

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    checkers = Checkers()
    app.exec_()

