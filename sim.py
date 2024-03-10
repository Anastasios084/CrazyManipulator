import pandas as pd
import numpy as np
import sys
sys.path.append('..')
from get_inference_data import *
import random
def open_model():
    print("opening model")


def preprocessed_data():
    print("processing data")

def next_draw():
    probabilities = [["CrazyTime", 0.0185], ["CoinFlip", 0.074], ["CashHunt", 0.037], ["Pachinko", 0.037], ["10", 0.074], ["5", 0.1295], ["2", 0.2405], ["1", 0.3885]]
    # probabilities = [["CT", 0.0185], ["CF", 0.074], ["CH", 0.037], ["P", 0.037], ["10", 0.074], ["5", 0.1295], ["2", 0.2405], ["1", 0.3885]]

    # Extract options and their corresponding probabilities
    options, probs = zip(*probabilities)

    # Choose a random option based on their probabilities
    random_choice = random.choices(options, weights=probs)[0]

    print("Randomly chosen option:", random_choice)
    return random_choice
    # # Create a 7x7 matrix filled with None
    # matrix = [[None for _ in range(7)] for _ in range(7)]
    # for i in range(7):
    #     for j in range(7):
    #         # Choose a random option based on their probabilities
    #         random_choice = random.choices(options, weights=probs)[0]
    #         matrix[i][j] = random_choice

    # for i in range(7):
    #     print(matrix[i][0] + " " + matrix[i][1] + " " + matrix[i][2] + " " +matrix[i][3] + " " + matrix[i][4] + " " + matrix[i][5] + " " + matrix[i][6])


def inference(df, hist):
    prev = []
    # for i in range(hist):
    #     prev.append(df.iloc[i]["resultSector"])
    
    probabilities = [["CrazyTime", 0.0185], ["CoinFlip", 0.074], ["CashHunt", 0.037], ["Pachinko", 0.037], ["10", 0.074], ["5", 0.1295], ["2", 0.2405], ["1", 0.3885]]
    # probabilities = [["CT", 0.0185], ["CF", 0.074], ["CH", 0.037], ["P", 0.037], ["10", 0.074], ["5", 0.1295], ["2", 0.2405], ["1", 0.3885]]

    # Extract options and their corresponding probabilities
    options, probs = zip(*probabilities)

    # Create a 7x7 matrix filled with None
    prev = []
    for i in range(hist):
        # Choose a random option based on their probabilities
        random_choice = random.choices(options, weights=probs)[0]
        prev.append(random_choice)


    # Count the occurrences of each option in the last draws
    counts = {option: prev.count(option) for option, _ in probabilities}

    # Calculate the total count of all options
    total_count = sum(counts.values())

    # Calculate the probabilities for the next turn based on the previous draws
    next_probabilities = []

    for option, prob in probabilities:
        if option in counts:
            next_prob = counts[option] / total_count
        else:
            next_prob = 0
        next_probabilities.append([option, next_prob])

    # Calculate the remaining probability to distribute among the options that did not appear
    remaining_probability = 1 - sum(prob for _, prob in next_probabilities)

    # Count the number of options that did not appear
    num_options_not_appeared = len(probabilities) - len(counts)

    # Distribute the remaining probability equally among the options that did not appear
    if num_options_not_appeared > 0:
        additional_prob_per_option = remaining_probability / num_options_not_appeared
        for option, prob in probabilities:
            if option not in counts:
                next_probabilities.append([option, additional_prob_per_option])

    print("Probabilities for the next turn:")
    for option, prob in next_probabilities:
        print(f"{option}: {prob:.4f}")

    return next_probabilities
    # print(prev)


def play_spin(bet, probs):
    winning_value = next_draw()
    winnings = 0
    for p in probs:
        if p[0] == winning_value:
            bet_on_winning = p[1]*bet
            if winning_value == "1":
                winnings =  bet_on_winning*2
            elif winning_value == "2":
                winnings =  bet_on_winning*3
            elif winning_value == "5":
                winnings =  bet_on_winning*6
            elif winning_value == "10":
                winnings =  bet_on_winning*11
            elif winning_value == "CoinFlip":
                winnings =  bet_on_winning*random.randint(2, 15)
            elif winning_value == "CashHunt":
                winnings =  bet_on_winning*random.randint(5, 100)
            elif winning_value == "CrazyTime":
                winnings =  bet_on_winning*random.randint(20, 150)
            elif winning_value == "CashHunt":
                winnings =  bet_on_winning*random.randint(10, 100)
    
    print("WINNINGS = " + str(winnings))

    return winnings


STARTING_BUDGET = 10000.0 # Give 1000 credits to the model to play 
CURRENT_BUDGET = STARTING_BUDGET
AVAILABLE_TURNS = 100 # Play for 100 turns
BET_PERCENTAGE = 0.2
HISTORY = 20
# inference(1)

for t in range(AVAILABLE_TURNS):
    df = get_inference_data(HISTORY) # get last N draws, for example 10
    probabilites = inference(df, HISTORY)

    print(probabilites)

    bet = CURRENT_BUDGET*BET_PERCENTAGE
    CURRENT_BUDGET -= bet

    winnings = play_spin(bet, probabilites)

    CURRENT_BUDGET += winnings
    print("Current BUDGET = " + str(CURRENT_BUDGET))
