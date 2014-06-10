#!/usr/bin/env python

import sys
import random

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    text = open(corpus)
    contents = text.read()
    list_text = contents.split()

    swift_dict = {}

    for i in range(len(list_text)-2):
        key = (list_text[i], list_text[i+1])
        if key in swift_dict:
            swift_dict[key] += [list_text[i+2]]
        else:
            swift_dict[key] = [list_text[i+2]]

    return swift_dict

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    start = random.choice(chains.keys())
    random_output = start[0] + ' ' + start[1]
    current_key = start

    while chains.get(current_key):
        next_word = random.choice(chains[current_key])
        current_key = (current_key[1], next_word)
        random_output += " %s" % next_word
    
    print random_output

def main():
    args = sys.argv

    input_text = args[1]
    chain_dict = make_chains(input_text)
    random_text = make_text(chain_dict)

if __name__ == "__main__":
    main()