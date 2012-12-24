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

pos = checkers.Position()
position_check(pos)

