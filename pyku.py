#!/usr/bin/python
#
# pyku
# ====
# Python-based random haiku generator
#
# Chris Collins, <christopher.collins@duke.edu>
#
# v0.5 - 2013-11-15
#
# Copyright 2013 Chris Collins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


debug = False
debug_word = ""

### TODO:###
# Unhandled Exceptions:
#   "ai" is two syllables
#   "ia" may be two syllables, eg. 'negotiated'
#   "oa" may be two syllables, eg. 'Croation'
#   "-ed" is usually silent, unless following double t"s
#   "-ier" is usually two syllables

### Import the necessary modules ###
# Import RE for regular expression matching
# Import random to grab random words
import re
if not debug_word:
    import random

### Set global variables ###
# The starting number of syllables
syllables = 0

# Our Random Word
glorand_word = ""


def pyku():
    """
    Build a Haiku
    """

    tonic = buildline(5)
    penultimate = buildline(7)
    ultimate = buildline(5)

    print tonic
    print penultimate
    print ultimate


def buildline(line_syllables):
    """
    Build each line from random words
    """
    line_list = []
    our_syllables = 0
    while (our_syllables < line_syllables):
        randomword()
        if debug:
            print glorand_word
        if (our_syllables + syllables) > line_syllables:
            randomword()
        else:
            print glorand_word
            print syllables
            line_list.append(glorand_word)
            our_syllables += syllables

        if debug:
            print "My Line Syllables:", line_syllables
            print "My Syllables So Far:", our_syllables

    return ' '.join(line_list)


def randomword():
    """
    Gets a random word from the Unix american-english dictionary
    """
    # Reset the syllable count
    syleq()

    if debug_word:
        random_word = debug_word
    else:
        # Open our word list
        text = open("/usr/share/dict/american-english")
        words = text.read()
        random_word = random.choice(words.split())

    if debug:
        print random_word

    check_possessive(random_word)


def check_possessive(random_word):
    """
    For now, we want to throw back possessive words.
    """
    poss = re.match(r".*'s", random_word, re.IGNORECASE)
    if poss:
        randomword()
    else:
        if debug:
            print "Our word is:", random_word
        global glorand_word
        glorand_word = random_word
        vowelfind(random_word)


def vowelfind(random_word):
    """
    Find the vowel clusters in the random word
    """
    vowel_list = "[aeiouy]+"
    vowels = re.findall(vowel_list, random_word, re.IGNORECASE)
    if vowels:
        vowelcount = len(vowels)
        if debug:
            print vowels
        global syllables
        syllables += vowelcount
        vowelcontext(random_word)
    else:
        randomword()


def vowelcontext(random_word):
    """
    Container module for  running through
    the list of checks we need to do to count
    syllables.
    """
    if debug:
        print "Going into 'vowelcontext':"
        print "Number of Syllables, maybe: ", syllables
    trailing_e(random_word)
    # Obsoleted by adding 'y' to vowel list
    # trailing_y(random_word)


def trailing_e(random_word):
    """
    First:
        Check if word ends in '-e', or optionally, '-es',
    not immediately preceeded by another vowel OR ending in '-que'
    AND  does  not end in '-ble' or '-ses', THEN decrements the
    syllable count.

    UNLESS - there is only 1 syllable.

    Cases:

        fare, faires, tree - matches first, does not decrement
        martinique - does not match first, does match second, decrements
        unibroue - does not match first or second, does not decrement

    # TODO - Unhandled Exceptions:

        fire - could be two syllables

    """
    # Finds trailing -e(s) WITHOUT preceeding vowels OR ending in '-que'
    #trail_e = re.findall(r"[^aeiou]+?e[s]?$", random_word, re.IGNORECASE)
    trail_e_que = re.findall(r"((qu)|([^aeiou]))+?e[s]?$",
                             random_word,
                             re.IGNORECASE)
    # Check for '-ble or -ses'
    trail_ses_ble = re.findall(r"((bl)|(s))e[s]?$",
                               random_word,
                               re.IGNORECASE)
    if trail_e_que and not trail_ses_ble:
        if debug:
            print trail_e_que
            print """
            Trailing '-e(s)' or '-que' characters
            and no trailing '-ble' or '-ses'."""
        syldec(1)
        if debug:
            print "Leaving 'trailing_e':"
            print "Number of Syllables, maybe: ", syllables

    modcount("trailing_e")


def sylinc(i):
    global syllables
    syllables += i


def syldec(i):
    global syllables
    if syllables > 1:  # Can't reduce to 0
        syllables -= i


def syleq():
    global syllables
    syllables = 0


def modcount(mod):
    if debug:
        print "Leaving '" + mod + "' - "
        print "Number of Syllables is, maybe: ", syllables


### Deprecated Code

# Was in trailing_e:

    # Deprecated with combined trail_e_que function
    #else:
    #    # Finds trailing -que(s)
    #    trail_que = re.findall(r"que[s]?$", random_word, re.IGNORECASE)
    #    if trail_que:
    #        if debug:
    #            print trail_que
    #            print "There is a trailing '-que'."
    #        syldec(1)
    #    else:  # Else no -e(s) OR -e(s) with preceeding vowels
    #        if debug:
    #            print "There is no trailing 'e(s)' character."

# Used to be trailing_y:

# Obsoleted by adding 'y' to vowel list
# def trailing_y(random_word):
#     """
#     Check to see if the word ends in '-y',
#     and is preceeded by a vowel, and
#     increment the syllable count
#     """
#     trail_y = re.findall(r"[^aeiou]+?y$", random_word)
#     if trail_y:
#         print trail_y
#         print "There is a trailing '-y' character."
#         sylinc(1)
#
#     modcount("trailing_y")

pyku()
