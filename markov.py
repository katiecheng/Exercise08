#!/usr/bin/env python

import sys
import random
import string

def make_chains(corpus1, corpus2):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    text1 = open(corpus1) # open files
    text2 = open(corpus2)
    
    contents1 = text1.read() # read file contents
    contents2 = text2.read()

    list_text1 = contents1.split() # split file contents into lists of words
    list_text2 = contents2.split()

    global dict1
    global dict2
    dict1 = {} # initialize dictionaries
    dict2 = {}

    for i in range(len(list_text1)-2): # populate dicts with tuples (bigrams)
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

    return [dict1, dict2] # return dictionaries

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    global has_miley
    global has_ernest
    switch = random.choice([0,1])
    check_miley_ernest(switch)

    random_tuple = check_upper(chains, switch)

    random_output = random_tuple[0] + ' ' + random_tuple[1]
    current_key = random_tuple

    while len(random_output) < 140:
        if chains[(switch + 1) % 2].get(current_key): # if the other dict has key, switch
            switch = (switch + 1) % 2
            try:
                next_word = random.choice(chains[switch][current_key])
                current_key = (current_key[1], next_word)
                random_output += " %s" % next_word
            except KeyError:
                break
        else: # else, stick with the same dict
            try:
                next_word = random.choice(chains[switch][current_key])
                current_key = (current_key[1], next_word)
                random_output += " %s" % next_word
            except KeyError:
                break
        check_miley_ernest(switch)

    if has_miley and has_ernest:
        return random_output
    else:
        return ''

def check_upper(chains, switch):
    random_tuple = random.choice(chains[switch].keys())

    while random_tuple[0][0] not in string.uppercase:
        random_tuple = random.choice(chains[switch].keys())
    
    return random_tuple

def check_miley_ernest(switch):
    global has_miley
    global has_ernest

    if switch == 0:
        has_miley = True
    else:
        has_ernest = True

def check_miley_ernest2(potential_output_string): #check final string for ernest and miley
    global dict1
    global dict2

    has_miley2 = False
    has_ernest2 = False

    list_text = potential_output_string.split()
    dict_tuples = {}

    for i in range(len(list_text)-1): # populate list with tuples (bigrams)
        key = (list_text[i], list_text[i+1])
        if key not in dict_tuples:
            dict_tuples[key] = None

    for bigram in dict_tuples:
        if bigram in dict1:
            has_miley2 = True
        if bigram in dict2:
            has_ernest2 = True

    if has_miley2 and has_ernest2:
        return True
    else:
        return False


def remove_end(rand_output):
    list_rand = []
    for char in rand_output:
        list_rand.append(char)
    backward_rand = list_rand[::-1]

    try:
        period_position = backward_rand.index('.')
        if period_position == 0:
            backward_rand.pop(0)
            period_position = backward_rand.index('.')
        remove_after_period = backward_rand[period_position:]
        return ''.join(remove_after_period[::-1])
    except ValueError:
        return []

def twitterize(rand_output):

    shortened_output = remove_end(rand_output)

    while len(shortened_output) > 140:
        shortened_output = remove_end(shortened_output)

    twitter_output = shortened_output
    return twitter_output

def final_output(twitter_text):
    if twitter_text != [] and check_miley_ernest2(twitter_text): 
    # If no text generated with periods, miley, and ernest, try again.
        return twitter_text
    else:
        main()


def main():
    global has_miley
    global has_ernest
    has_miley = False
    has_ernest = False

    input_text1 = 'miley.txt'
    input_text2 = 'ernest.txt'

    chain_list = make_chains(input_text1, input_text2)
    random_text = make_text(chain_list)
    twitter_text = twitterize(random_text)
    return final_output(twitter_text)

if __name__ == "__main__":
    main()