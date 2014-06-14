#-------------------------------------------------------------------------------
# Name:         markov.py
# Purpose:      Hackbright Exercise08: Markov Twitterbot
#
# Author:       Katie Cheng and Maggie Shine
# Date:         06/13/2014
#
# Reads in text from two sources, mashes text together, and returns a twitter-
# ready string. String is less than 140 characters, begins with a capital 
# letter, and ends with a period.
#-------------------------------------------------------------------------------

import random
import time
import string

def make_chains(corpus1, corpus2):

    """Takes two input texts as a string and returns two dictionaries of
    markov chains."""

    text1 = open(corpus1) # open files
    text2 = open(corpus2)
    
    contents1 = text1.read() # read file contents
    contents2 = text2.read()

    list_text1 = contents1.split() # split file contents into lists of words
    list_text2 = contents2.split()

    global DICT1
    global DICT2
    DICT1 = {} # initialize two dictionaries, one for each text
    DICT2 = {}

    for i in range(len(list_text1)-2): # populate DICT1 with tuples (bigrams)
        key = (list_text1[i], list_text1[i+1])
        if key in DICT1:
            DICT1[key] += [list_text1[i+2]] # if key exists, add to value list
        else:
            DICT1[key] = [list_text1[i+2]] # else, assign key to value list

    for i in range(len(list_text2)-2): # populate DICT2 with tuples
        key = (list_text2[i], list_text2[i+1])
        if key in DICT2:
            DICT2[key] += [list_text2[i+2]]
        else:
            DICT2[key] = [list_text2[i+2]]

    return [DICT1, DICT2] # return dictionaries

def make_text(chains):

    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    global HAS_MILEY
    global HAS_ERNEST

    # create "switch" to allow forced switching between DICT1 and DICT2
    switch = random.choice([0, 1]) # set initial "switch" value to 0 or 1

    check_miley_ernest(switch) # call check_miley_ernest() function

    random_tuple = check_upper(chains, switch) # choose a random starting tuple

    random_output = random_tuple[0] + ' ' + random_tuple[1]
    current_key = random_tuple

    while len(random_output) < 140:
        if chains[(switch + 1) % 2].get(current_key): 
        # if the other DICT has key, grab next_word value from the other DICT
            switch = (switch + 1) % 2
            try:
                next_word = random.choice(chains[switch][current_key])
                current_key = (current_key[1], next_word) # set the new tuple
                random_output += " %s" % next_word # append next_word to output
            except KeyError: # KeyError may occur if tuple is not a key in DICT
                break
        else: # else, stick with the same DICT and grab a random next_word value
            try:
                next_word = random.choice(chains[switch][current_key])
                current_key = (current_key[1], next_word) # set the new tuple
                random_output += " %s" % next_word # append next_word to output
            except KeyError: # KeyError may occur if tuple is not a key in DICT
                break
        check_miley_ernest(switch) # call check_miley_ernest() function

    if HAS_MILEY and HAS_ERNEST: # if both HAS_MILEY and HAS_ERNEST are true...
        return random_output # return random_output
    else:   # else, return the empty string
        return ''

def check_upper(chains, switch):

    """Make sure that the randomly-selected first tuple begins with an 
    Uppercase character (to approximate the syntax of an English sentence.)"""

    random_tuple = random.choice(chains[switch].keys()) # pick a random tuple 

    # keep picking until the random tuple begins with a capital letter
    while random_tuple[0][0] not in string.uppercase: 
        random_tuple = random.choice(chains[switch].keys())
    
    return random_tuple # return the random tuple

def check_miley_ernest(switch):

    """Checks if output string contains tuples from both Miley and Ernest"""

    global HAS_MILEY
    global HAS_ERNEST

    if switch == 0: # When switch is 0, string contains at least 1 Miley tuple
        HAS_MILEY = True # Therefore, set HAS_MILEY to True. 
    else: # Else (when switch is 1), the string contains at least 1 Ernest tuple
        HAS_ERNEST = True # Therefore, set has_earnest to True

def check_miley_ernest2(potential_output_string): 

    """Check final string for Ernest and Miley. (This second check is necessary
        because some of the text is removed in remove_end(), and this might
        remove all occurrences of text from either Ernest or Miley."""

    global DICT1
    global DICT2

    has_miley2 = False # variable is local to the check_miley_ernest2() func
    has_ernest2 = False # variable is local to the check_miley_ernest2() func

    list_text = potential_output_string.split() # split string into word list
    dict_tuples = {} # initialize an empty dictionary (could have used a list)
    # arbitrarily chose a dictionary because it's (insignificantly) faster

    for i in range(len(list_text)-1): # populate dict with tuples (bigrams)
        key = (list_text[i], list_text[i+1]) # key is a tuple
        if key not in dict_tuples: # if the key is not already in the dict...
            dict_tuples[key] = None # add the tuple:None key:value pair

    # for each tuple, if it's in the Miley DICT1 or the Ernest DICT2, set the 
    # respective has_miley2 and has_ernest2 variables to True
    for bigram in dict_tuples: 
        if bigram in DICT1:
            has_miley2 = True
        if bigram in DICT2:
            has_ernest2 = True

    # return whether both has_miley2 and has_ernest2 are True
    if has_miley2 and has_ernest2: 
        return True
    else:
        return False

def twitterize(rand_output):

    """ 'Twitterize' the output by removing 'complete phrases' (phrases ending 
        with a period '.') until the string is less than 140 characters"""

    shortened_output = remove_end(rand_output) # remove chars after the last '.'

    # continue to remove phrases until output is less than 140 characters long
    while len(shortened_output) > 140: 
        shortened_output = remove_end(shortened_output)

    twitter_output = shortened_output
    return twitter_output # once it's less than 140 characters, return output

def remove_end(rand_output):

    """Removes end of the string that occurs after the final period '.' An
    attempt to make the phrases generated sound more complete"""

    list_rand = [] # initialize an empty list

    for char in rand_output: # for each char in string, append char to list_rand
        list_rand.append(char)

    backward_rand = list_rand[::-1] # create new variable, the list backwards

    try:
        period_position = backward_rand.index('.') # return index of first '.'
        if period_position == 0: # if the index is 0 (meaning it's the 1st char)
            backward_rand.pop(0) # pop that '.' and find the index of the next
            period_position = backward_rand.index('.')

        # once index is found, slice the list from 1st period to the end
        remove_after_period = backward_rand[period_position:]

        # flip the backwards list forward again, and join it back into a string
        return ''.join(remove_after_period[::-1]) # return that value

    except ValueError: # Except when ValueError (if there is no '.' character)
        return [] # return an empty list

def final_output(twitter_text, start):

    """Check again whether 'twitterized' string contains both Miley and Ernest,
    and contains at least one complete phrase. If so, return twitter_text"""

    if twitter_text != [] and check_miley_ernest2(twitter_text): 
    # If no text generated with periods, miley, and ernest, try again.
        print time.time()-start # print text-generation time -just for reference
        return twitter_text
    else:
        return main() 
        # if twitter_text does not satisfy conditions, call main() again


def main():

    """Main function"""

    start = time.time() # just to check how long it takes for the script to run

    global HAS_MILEY
    global HAS_ERNEST
    HAS_MILEY = False # initialize HAS_ MILEY and HAS_ERNEST as False by default
    HAS_ERNEST = False

    input_text1 = 'miley.txt' # hardcode input text
    input_text2 = 'ernest.txt'

    chain_list = make_chains(input_text1, input_text2) # create DICT1 and DICT2
    random_text = make_text(chain_list) # generate a mashup text 
    twitter_text = twitterize(random_text) # curate the text for twitter
    return final_output(twitter_text, start) # return the final output


if __name__ == "__main__":
    main()