#!/usr/bin/env python2
"""Unit tests for the various classes"""
import checkers


def position_check(pos_object):
    """Test whether position objects are working properly"""
    def check_coord(exp_x, exp_y, pos):
        return (exp_x == pos.get_x() and exp_y == pos.get_y())

    cur_x = pos_object.get_x()
    cur_y = pos_object.get_y()

    pos_object.move(checkers.NW)
    print check_coord(cur_x + 1, cur_y + 1, pos_object)  #false
    pos_object.move(checkers.SE)
    print check_coord(cur_x, cur_y, pos_object)          #true
    pos_object.move(checkers.NE)
    print check_coord(cur_x - 1, cur_y + 1, pos_object)  #false
    pos_object.move(checkers.SW)
    print check_coord(cur_x, cur_y, pos_object)          #true

def board_test(board):
    def draw_board(board, width, height):
        for piece in board:
            if board[piece]:
                print board[piece],
            else:
                print "-",

            if piece in [i - 1 for i in range(0, width * height, width)]:
                print

    print board
    print "\n"
    print board.squares[2 * board.width + 1]
    print board.squares[3 * board.width]
    print board.move((1, 2), (0, 3))
    print board
    print "\n"
    print board.squares[5 * board.width + 2]
    print board.squares[4 * board.width + 1]
    print board.move((2, 5), (1, 4))
    print board
    print "\n"
    print board.squares[3 * board.width + 0]
    print board.squares[4 * board.width + 1]
    print board.squares[5 * board.width + 2]
    print board.jump((0, 3), (1, 4), (2, 5))
    print board
    print "\n"
    board.squares[1] = checkers.Piece("red")
    print board
    print "\n"
    print board.crown((1, 0))
    print board

board_test(checkers.Board())

