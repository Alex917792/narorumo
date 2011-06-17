#!/usr/bin/env python3

import sys

def get_opponent_move():
    option = input().strip()
    one = input().strip()
    two = input().strip()
    if option == "1":
        card, slot = one, two
    elif option == "2":
        card, slot = two, one
    else:
        assert False, "option is neither one nor two?!"
    return option, card, slot

def playzero():
    """
    Do a right application of our slot 0 to the zero card.  This
    writes the value of ((lambda (x) x) 0), which is to say, 0, into
    our slot 0.
    """
    print("2")
    print("0")
    print("zero")

def playdec():
    """
    Do a left application of the dec card to our slot 0.  This
    side-effects the opponent's (255-0)th slot (that is, their 255th
    slot), decrementing its vitality by 1, and returns the identity
    function (causing our slot 0 to be overwritten by the identity
    function again).
    """
    print("1")
    print("dec")
    print("0")

def main():
    whoami = sys.argv[1]
    if whoami == "1":
        get_opponent_move()

    turn = 0
    while True:
        try:
            if turn % 2 == 0:
                playzero()
            else:
                playdec()
            option, card, slot = get_opponent_move()
            turn += 1
        except EOFError as e:
            return

if __name__ == "__main__": main()