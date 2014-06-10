#!/usr/bin/env python

import sys
import random

def make_chains(corpus1, corpus2):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    text1 = open(corpus1)
    text2 = open(corpus2)
    
    contents1 = text1.read()
    contents2 = text2.read()

    list_text1 = contents1.split()
    list_text2 = contents2.split()

    dict1 = {}
    dict2 = {}

    for i in range(len(list_text1)-2):
        key = (list_text1[i], list_text1[i+1])
        if key in dict1:
            dict1[key] += [list_text1[i+2]]
        else:
            dict1[key] = [list_text1[i+2]]

    for i in range(len(list_text2)-2):
        key = (list_text2[i], list_text2[i+1])
        if key in dict2:
            dict2[key] += [list_text2[i+2]]
        else:
            dict2[key] = [list_text2[i+2]]

    return [dict1, dict2]

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
    script, input_text1, input_text2 = args
    chain_dict = make_chains(input_text1, input_text2)
    # random_text = make_text(chain_dict)

if __name__ == "__main__":
    main()