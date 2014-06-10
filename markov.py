#!/usr/bin/env python

import sys
import random

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    text = open(corpus)

    list_text = []

    for line in text:
        list_text += line.rstrip().split(" ")
        # print list_text

    swift_dict = {}

    for i in range(len(list_text)-2):
        key = (list_text[i], list_text[i+1])
        # check if key already exists in dict
        # if yes, add value to list of values
        if key in swift_dict:
            swift_dict[key] += [list_text[i+2]]
        # if not, add new key:value pair
        else:
            swift_dict[key] = [list_text[i+2]]

    return swift_dict

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    # for key, value in chains.iteritems():

    random_output = ''
    current_key = random.choice(chains.keys())

    while current_key in chains.keys():
        next_word = random.choice(chains[current_key])
        current_key = (current_key[1], next_word)
        random_output += " %s" % next_word
        print random_output



def main():
    args = sys.argv

    # Read input_text from a file
    input_text = args[1]
    chain_dict = make_chains(input_text)
    random_text = make_text(chain_dict)
    # print random_text

if __name__ == "__main__":
    main()