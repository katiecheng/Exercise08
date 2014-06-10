#!/usr/bin/env python

import sys

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    text = open(corpus)

    list_text = []

    for line in text:
        list_text += line.rstrip().split(" ")
        # print list_text

    swift_dict = {}

    for i in range(len(list_text)-1):
        key = (list_text[i], list_text[i+1])
        swift_dict[key] = [None]
        # check if key already exists in dict
        # if yes, add value to list of values
        # if no, add new key:value pair

    print swift_dict

    return {}

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    return "Here's some random text."

def main():
    args = sys.argv
    make_chains("trouble_swift.txt")
    # Change this to read input_text from a file
    # input_text = "Some text"

    # chain_dict = make_chains(input_text)
    # random_text = make_text(chain_dict)
    # print random_text

if __name__ == "__main__":
    main()