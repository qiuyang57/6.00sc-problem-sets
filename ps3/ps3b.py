from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    for j in range(HAND_SIZE,0,-1):
        perms = get_perms(hand, j)
        for i in range(len(perms)):
            if is_valid_word(perms[i], hand, word_list):
                return perms[i]
    return None
            

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...
    n = calculate_handlen(hand)
    sum_score = 0
    hand_updated = hand
    display_hand(hand)
    while calculate_handlen(hand_updated) > 0:
        word = comp_choose_word(hand_updated, word_list)
        if word == None:
            break
        word_score = get_word_score(word, n)
        hand_updated = update_hand(hand_updated, word)
        print '%s earned %d points.' %(word,word_score)
        sum_score += word_score
    print 'Total: %d points' %sum_score
    
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    hand = {}
    while True:
        order = raw_input("'n', 'r', 'e'")
        if order == 'n' or hand == {}:
            hand = deal_hand(HAND_SIZE)
            while True:
                order1 = raw_input("'u', 'c'")
                if order1 == 'u':
                    play_hand(hand, word_list)
                elif order1 == 'c':
                    comp_play_hand(hand, word_list)
                    break
        elif order == 'r':
            while True:
                order1 = raw_input("'u', 'c'")
                if order1 == 'u':
                    play_hand(hand, word_list)
                elif order1 == 'c':
                    comp_play_hand(hand, word_list)
                    break
        elif order == 'e':
            break

        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    HAND_SIZE = 7
    play_game(word_list)



    
