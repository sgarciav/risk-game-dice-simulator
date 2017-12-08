#!/usr/bin/env python

# pylint: disable=C0103
""" Author: Sergio Garcia-Vergara """

import sys
import math
import numpy as np
import argparse
import random


def max_dice(s):
    return {
        'attacker': 3,
        'defender': 2
    }.get(s, 0)

class DiceData:
    """ data structure for dice objects """
    def __init__(self, team, num_troops):
        self.num_troops = num_troops
        self.team = team
        self.num_dice = None
        self.max_dice = max_dice(team)
        self.vals = []


# global variables

# user-defined functions
# ---------------------------------------
# ---------------------------------------

# -----------------------
def parse_arguments():
    ''' parse through command line arguments '''
    global args_

    parser = argparse.ArgumentParser(description='Roll RISK DiceData.')

    # required values
    parser.add_argument(
        "attacker_troops",
        type=int,
        help="Number of troops attacker team has."
    )
    parser.add_argument(
        "defender_troops",
        type=int,
        help="Number of troops defender team has."
    )

    # optional
    parser.add_argument(
        "--verbose",
        type=str2bool, default=True,
        help="Run without displaying progress."
    )

    args_ = parser.parse_args()

    # make sure number of troops makes sense
    if (args_.attacker_troops < 2 or args_.defender_troops < 1):
        print 'NO CHEATING.'
        print 'attacker troops: ' + str(args_.attacker_troops) + ' | min: 2'
        print 'defender troops: ' + str(args_.defender_troops) + ' | min: 1'
        sys.exit()


# -----------------------
def str2bool(v):
    ''' string to bool '''
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


# main loop
# =======================================
def main_loop():
    ''' main loop '''

    # parse through arguments
    parse_arguments()

    attacker = DiceData('attacker', args_.attacker_troops)
    defender = DiceData('defender', args_.defender_troops)

    # get number of dice each team has
    attacker.num_dice = attacker.max_dice if attacker.num_troops > attacker.max_dice else attacker.num_troops - 1
    defender.num_dice = defender.max_dice if defender.num_troops > defender.max_dice else defender.num_troops

    if (args_.verbose):
        print '-- attacker attacking with ' + str(attacker.num_dice) + ' rolls'
        print '-- defender attacking with ' + str(defender.num_dice) + ' rolls'

    # generate dice rolls
    for i in range(0, attacker.num_dice):
        d = random.randint(1,6)
        attacker.vals.append(d)

    for i in range(0, defender.num_dice):
        d = random.randint(1,6)
        defender.vals.append(d)

    # sort dice rolls
    attacker.vals.sort()
    defender.vals.sort()

    # compare rolls
    m = min(len(attacker.vals), len(defender.vals))


if __name__ == '__main__':
    main_loop()
