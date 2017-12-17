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
        self.max_dice = max_dice(self.team)
        self.rolls = []
        self.W = 0


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
        "--quiet",
        action='store_true',
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
def resetFields(group):
    ''' Update the team parameters as setup for the next battle '''

    group.W = 0
    group.rolls = []
    return group


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

    next_battle = True
    battles_fought = 0

    while next_battle:

        # reset fields
        attacker = resetFields(attacker)
        defender = resetFields(defender)

        # get number of dice each team has
        attacker.num_dice = attacker.max_dice if attacker.num_troops > attacker.max_dice else attacker.num_troops - 1
        defender.num_dice = defender.max_dice if defender.num_troops > defender.max_dice else defender.num_troops

        # TODO: move these repeating events to separate function

        # generate dice rolls
        for i in range(0, attacker.num_dice):
            d = random.randint(1,6)
            attacker.rolls.append(d)

        for i in range(0, defender.num_dice):
            d = random.randint(1,6)
            defender.rolls.append(d)

        # sort dice rolls from max to min
        attacker.rolls.sort(reverse=True)
        defender.rolls.sort(reverse=True)

        # count wins for each team
        for i in range(0, min(len(attacker.rolls), len(defender.rolls))):
            if attacker.rolls[i] > defender.rolls[i]:
                attacker.W += 1
            else:
                defender.W +=1

        # update number of troops based on rolls
        attacker.num_troops -= defender.W
        defender.num_troops -= attacker.W

        battles_fought += 1

        # print results
        print ''
        print 'Battle #' + str(battles_fought)
        print '================================================'

        if args_.quiet:
            print '-- Attacker remaining troops: ' + str(attacker.num_troops)
            print '-- Defender remaining troops: ' + str(defender.num_troops)
            print ''
        else:
            print ''
            print 'Attacker'
            print '----------------'
            print '-- attacked with ' + str(attacker.num_dice) + ' rolls'
            print '-- rolls: ' + str(attacker.rolls) + ' --> wins: ' + str(attacker.W)
            print '-- remaining troops: ' + str(attacker.num_troops)
            print ''
            print 'Defender'
            print '----------------'
            print '-- defended with ' + str(defender.num_dice) + ' rolls'
            print '-- rolls: ' + str(defender.rolls) + ' --> wins: ' + str(defender.W)
            print '-- remaining troops: ' + str(defender.num_troops)
            print ''

        # automatically stop if a team loses all of its troops
        if attacker.num_troops < 2 or defender.num_troops <= 0:
            next_battle = False
            continue

        # ask user if they want to continue or stop
        r = raw_input("Go on to next battle? [Y/n]: ") or "Y"
        next_battle = str2bool(r)

    # END
    print '============================'
    print '         WAR HAS ENDED      '
    print '============================'


if __name__ == '__main__':
    main_loop()
