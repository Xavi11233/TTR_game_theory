import random
import itertools
import numpy as np
import nashpy as nash
import scipy.stats as stats
import matplotlib.pyplot as plt

# Initialising the possible routes we can select, with shortest possible routes between each 2 destinations on route cards.

Lisboa_Danzic = ["Lisboa", "Madrid", "Pamplona", "Paris", "Frankfurt", "Berlin", "Danzic"]
Brest_Petrograd_Normal = ["Brest", "Paris", "Frankfurt", "Berlin", "Danzic", "Riga", "Petrograd"]
Brest_Petrograd_Long = ["Brest", "Paris", "Frankfurt", "Essen", "Kobenhaven", "Stockholm", "Petrograd"]
Palermo_Moskva = ["Palermo", "Smyrna", "Constantinople", "Bucuresti", "Kyiv", "Smolensk", "Moskva"]
Kobenhaven_Erzurum = ["Kobenhaven", "Essen", "Berlin", "Wien", "Budapest", "Bucuresti", "Sevastopol", "Erzurum"]
Edinburgh_Athina = ["Edinburgh", "London", "Amsterdam", "Frankfurt", "Munchen", "Venezia", "Roma", "Brindisi", "Athina"]
Cadiz_Stockholm = ["Cadiz", "Madrid", "Pamplona", "Paris", "Frankfurt", "Essen", "Kobenhaven", "Stockholm"]

Frankfurt_Smolensk = ["Frankfurt", "Berlin", "Warzawa", "Wilno", "Smolensk"]
Amsterdam_Wilno = ["Amsterdam", "Essen", "Berlin", "Warzawa", "Wilno"]
Berlin_Moskva = ["Berlin", "Warzawa", "Wilno", "Smolensk", "Moskva"]
Stockholm_Wien = ["Stockholm", "Kobenhaven", "Essen", "Berlin", "Wien"]
Athina_Wilno = ["Athina", "Sofia", "Bucuresti", "Kyiv", "Wilno"]
London_Wien = ["London", "Amsterdam", "Frankfurt", "Munchen", "Wien"]
Venezia_Constantinople = ["Venezia", "Zagrab", "Sarajevo", "Sofia", "Constantinople"]
Essen_Kyiv = ["Essen", "Berlin", "Warzawa", "Kyiv"]
Riga_Bucuresti = ["Riga", "Wilno", "Kyiv", "Bucuresti"]
Angora_Kharkov = ["Angora", "Erzurum", "Sochi", "Rostov", "Kharkov"]
Berlin_Roma = ["Berlin", "Frankfurt", "Munchen", "Venezia", "Roma"]
Bruxelles_Danzic = ["Bruxelles", "Frankfurt", "Berlin", "Danzic"]
Berlin_Bucuresti = ["Berlin", "Wien", "Budapest", "Bucuresti"]
Madrid_Zurich = ["Madrid", "Barcelona", "Marseille", "Zurich"]
Kyiv_Sochi = ["Kyiv", "Kharkov", "Rostov", "Sochi"]
Marseille_Essen = ["Marseille", "Zurich", "Munchen", "Frankfurt", "Essen"]
Smolensk_Rostov = ["Smolensk", "Moskva", "Kharkov", "Rostov"]
Brest_Venezia = ["Brest", "Paris", "Zurich", "Venezia"]
Barcelona_Munchen = ["Barcelona", "Marseille", "Zurich", "Munchen"]
Paris_Wien = ["Paris", "Frankfurt", "Munchen", "Wien"]
Barcelona_Bruxelles = ["Barcelona", "Pamplona", "Paris", "Bruxelles"]
Madrid_Dieppe = ["Madrid", "Pamplona", "Paris", "Dieppe"]
Sarajevo_Sevastopol = ["Sarajevo", "Sofia", "Bucuresti", "Sevastopol"]
Palermo_Constantinople = ["Palermo", "Smyrna", "Constantinople"]
Roma_Smyrna = ["Roma", "Brindisi", "Athina", "Smyrna"]
Amsterdam_Pamplona = ["Amsterdam", "Bruxelles", "Paris", "Pamplona"]
Edinburgh_Paris = ["Edinburgh", "London", "Dieppe", "Paris"]
London_Berlin = ["London", "Amsterdam", "Essen", "Berlin"]
Brest_Marseille = ["Brest", "Paris", "Marseille"]
Paris_Zagrab = ["Paris", "Zurich", "Venezia", "Zagrab"]
Zagrab_Brindisi = ["Zagrab", "Venezia", "Roma", "Brindisi"]
Warzawa_Smolensk = ["Warzawa", "Wilno", "Smolensk"]
Zurich_Budapest = ["Zurich", "Venezia", "Zagrab", "Budapest"]
Zurich_Brindisi = ["Zurich", "Venezia", "Roma", "Brindisi"]
Kyiv_Petrograd = ["Kyiv", "Wilno", "Petrograd"]
Sofia_Smyrna = ["Sofia", "Athina", "Smyrna"]
Rostov_Erzurum = ["Rostov", "Sochi", "Erzurum"]
Frankfurt_Kobenhaven = ["Frankfurt", "Essen", "Kobenhaven"]
Budapest_Sofia = ["Budapest", "Sarajevo", "Sofia"]
Athina_Angora = ["Athina", "Smyrna", "Angora"]

short_routes = [Frankfurt_Smolensk, Amsterdam_Wilno, Berlin_Moskva, Stockholm_Wien, Athina_Wilno, London_Wien, Venezia_Constantinople, 
                    Essen_Kyiv, Riga_Bucuresti, Angora_Kharkov, Berlin_Roma, Bruxelles_Danzic, Berlin_Bucuresti, Madrid_Zurich, Kyiv_Sochi, 
                    Marseille_Essen, Smolensk_Rostov, Brest_Venezia, Barcelona_Munchen, Paris_Wien, Barcelona_Bruxelles, Madrid_Dieppe, 
                    Sarajevo_Sevastopol, Palermo_Constantinople, Roma_Smyrna, Amsterdam_Pamplona, Edinburgh_Paris, London_Berlin, 
                    Brest_Marseille, Paris_Zagrab, Zagrab_Brindisi, Warzawa_Smolensk, Zurich_Budapest, Zurich_Brindisi, Kyiv_Petrograd, 
                    Sofia_Smyrna, Rostov_Erzurum, Frankfurt_Kobenhaven, Budapest_Sofia, Athina_Angora]

long_routes = [Lisboa_Danzic, Palermo_Moskva, Kobenhaven_Erzurum, Edinburgh_Athina, Cadiz_Stockholm, Brest_Petrograd_Normal]
long_routes_BPL = [Lisboa_Danzic, Palermo_Moskva, Kobenhaven_Erzurum, Edinburgh_Athina, Cadiz_Stockholm, Brest_Petrograd_Long]

def randomise_deck():
    """
    A function to draw a given number of cards from a randomised standard ticket to ride deck of cards.
    """
    colours = ["red", "orange", "yellow", "green", "blue", "purple", "white", "black"]
    deck = colours * 12 + ["rainbow"] * 14
    random.shuffle(deck)
    return deck

def get_specific_wanted_card(wanted_card="orange"):
    """
    A function to find if a specific wanted card (no-rainbow) is pulled from the 5 shown cards and then if not then the 2 random pulls 
    afterwards.
    """
    revealed_five_cards = []
    randomised_deck = randomise_deck()
    for i in range(5):
        revealed_five_cards.append(randomised_deck[0])
        randomised_deck.append(randomised_deck[0])
        del randomised_deck[0]
    if wanted_card in revealed_five_cards:
        return True
    else:
        if randomised_deck[0] == wanted_card or randomised_deck[1] == wanted_card or randomised_deck[0] == "rainbow" or randomised_deck[1] == "rainbow":
            return True
        else:
            return False

def chances_of_getting_specific_wanted_card(wanted_card="orange", repetitions=100):
    """
    A function to find the odds of getting a specific card colour from the shown 5 and the randomised unseen deck.
    """
    successful_pulls = 0
    for i in range(repetitions):
        if get_specific_wanted_card(wanted_card=wanted_card) == True:
            successful_pulls += 1
    return (successful_pulls / repetitions)

def completing_short_routes():
    """
    A function to find aveage route track length and average route reward from the lists.
    """
    short_route_scores = [5] * 5 + [6] * 5 + [7] * 5 + [8] * 13 + [9] * 2 + [10] * 5 + [11] * 2 + [12] * 2 + [13]
    short_route_totals = [11] * 5 + [12] * 3 + [14] + [15] * 3 + [16] + [17] * 2 + [18] * 3 + [19] * 8 + [20] * 3 + [22] * 3 + [23] + [25] + [26] * 3 + [29] * 2 + [32]
    average_route_reward = sum(short_route_totals) / 40
    average_route_track_length = (sum(short_route_scores) - 1) / 40
    return average_route_track_length, average_route_reward

def initial_short_route_selection(number_of_short_routes=3):
    """
    A function to simulate the random selection of 3 random short routes for player1 and player2.
    """
    player1 = []
    player2 = []
    chosen_routes = random.sample(short_routes, k=2 * number_of_short_routes)
    for i in range(number_of_short_routes):
        player1.append(chosen_routes[i])
    for j in range(number_of_short_routes, 2 * number_of_short_routes):
        player2.append(chosen_routes[j])
    return player1, player2

def check_for_blocking(selected_routes_player1, selected_routes_player2):
    """
    A function to check if there are any parts of routes that are blocked by another player playing their own routes.
    """
    intersecting_routes = []
    number_of_blockages = 0
    for i in range(len(selected_routes_player1)):
         for j in range(len(selected_routes_player2)):
                if selected_routes_player1[i - 1] != selected_routes_player2[j - 1]:
                    intersecting_routes.append(list(set(selected_routes_player1[i - 1]).intersection(selected_routes_player2[j - 1])))
    for k in intersecting_routes:
        if (len(k) - 1) > 0:
            number_of_blockages += (len(k) - 1)
    return number_of_blockages

def average_blocks(number_of_short_routes=3, repetitions=10_000, inc_long_routes=True):
    """
    A function to run a large simulation of players selecting random route cards and averaging the number of blocks that will occur, thus 
    finding the chances of a player unintentionally blocking another by following their route.
    """
    blockages = 0
    selected_long_routes = []
    for i in range(repetitions):
        selected_routes_player1, selected_routes_player2 = initial_short_route_selection(number_of_short_routes=number_of_short_routes)
        if inc_long_routes == True:
            selected_long_routes.append(random.sample(long_routes, k=2))
            selected_routes_player1.append(selected_long_routes[0][0])
            selected_routes_player2.append(selected_long_routes[0][1])
        blockages += check_for_blocking(selected_routes_player1=selected_routes_player1, selected_routes_player2=selected_routes_player2)
    return (blockages / repetitions)

def probability_of_block(number_of_short_routes=3, repetitions=10000):
    """
    A function to run a large simulation of players selecting random route cards and finding the chance of a block in each piece of track.
    """
    return average_blocks(number_of_short_routes=number_of_short_routes, repetitions=repetitions) / ((number_of_short_routes * 3.025) + (1 * 40 / 6))

def crossover_between_routes(selected_routes_of_player):
    """
    A function to find the amount of routes which crossover in a given players deck.
    """
    intersecting_routes = []
    number_of_crossovers = 0
    counter_of_intersecting_routes = []
    counter_of_intersecting_routes2 = []
    for i in range(len(selected_routes_of_player)):
            for j in range(len(selected_routes_of_player)):
                    if selected_routes_of_player[i - 1] != selected_routes_of_player[j - 1]:
                        intersecting_routes.append(list(set(selected_routes_of_player[i - 1]).intersection(selected_routes_of_player[j - 1])))
    #print(intersecting_routes)
    for i in intersecting_routes:
        if len(i) > 1:
            counter_of_intersecting_routes.append({'route': tuple(i), 'length': len(i) - 1, 'count': intersecting_routes.count(i) / 2})
    for j in counter_of_intersecting_routes:
        if j not in counter_of_intersecting_routes2:
            counter_of_intersecting_routes2.append(j)
    for k in counter_of_intersecting_routes2:
        for q in counter_of_intersecting_routes2:
            if list(k['route']) != list(q['route']) and list(set(k['route']).intersection(set(q['route']))) == list(k['route']):
                k['count'] -= 1
    for p in counter_of_intersecting_routes2:
        number_of_crossovers += int(p['count'] * p['length'])
    return number_of_crossovers

def average_crossover_between_routes(number_of_short_routes=3, repetitions=10_000, inc_long_routes=True):
    """
    A function to run a large simulation to find the average number of corrovers between routes in one players deck.
    """
    crossovers = 0
    selected_long_routes = []
    for i in range(repetitions):
        selected_routes_player1, selected_routes_player2 = initial_short_route_selection(number_of_short_routes=number_of_short_routes)
        if inc_long_routes == True:
            selected_long_routes.append(random.sample(long_routes, k=2))
            selected_routes_player1.append(selected_long_routes[0][0])
            selected_routes_player2.append(selected_long_routes[0][1])
        crossovers += crossover_between_routes(selected_routes_of_player=selected_routes_player1)
    return (crossovers / repetitions)

def probability_of_crossover(number_of_short_routes=3, repetitions=10_000):
    """
    A function to run a large simulation of selecting random route cards and finding the chance the player will have some crossover in 
    their hand.
    """
    return average_crossover_between_routes(number_of_short_routes=number_of_short_routes, repetitions=repetitions) / ((number_of_short_routes * 2.95) + (1 * 40 / 6))

def probability_of_completable_routes(repetitions=100, inc_long_routes=True, number_of_pieces=45, 
                                      expected_blocks_subtract_expected_crossovers=-0.5442156418048748):
    """
    A function to find the chance that a randomly selected route is statistically likely to be completed considering the 
    chances of blocking and crossovers:
    BPN has expected_blocks_subtract_expected_crossovers = -0.5442156418048748 which is expected loss of pieces in game.
    BPL has expected_blocks_subtract_expected_crossovers = 0.4405625615099315 which is expected loss of pieces in game.
    """
    short_route_lengths = [5] * 5 + [6] * 5 + [7] * 5 + [8] * 13 + [9] * 3 + [10] * 4 + [11] * 2 + [12] * 2 + [13]
    if inc_long_routes == True:
        long_route_lengths = [20] * 4 + [21] * 2
    else:
        long_route_lengths = [0]
    completed_routes = 0
    for i in range(repetitions):
        selected_long_route = random.sample(long_route_lengths, k=1)
        selected_short_routes = random.sample(short_route_lengths, k=3)
        total_route_lengths = sum(selected_long_route) + sum(selected_short_routes)
        if total_route_lengths + expected_blocks_subtract_expected_crossovers <= number_of_pieces:
            completed_routes += 1
    return (completed_routes / repetitions)

def find_lowest_cost_route(routes_in_hand=3, repetitions=100):
    """
    A function to find the average lowest cost route from a random hand from simulating it repeatedly.
    """
    short_route_rewards = [5] * 5 + [6] * 5 + [7] * 5 + [8] * 13 + [9] * 2 + [10] * 5 + [11] * 2 + [12] * 2 + [13]
    shortest_route_sums = 0
    for i in range(repetitions):
        selected_short_routes = random.sample(short_route_rewards, k=routes_in_hand)
        shortest_route = min(selected_short_routes)
        shortest_route_sums += shortest_route
    return (shortest_route_sums / repetitions)

def crossover_of_long_journeys_with_everything_else(long_journey):
    """
    A function to calculate the amount of times that a given long journey crosses over with any given short journey.
    """
    blocks = 0
    for i in short_routes:
        blocks += check_for_blocking(selected_routes_player1=[long_journey], selected_routes_player2=[i])
    return blocks / 40

def number_of_equal_length_routes(selected_route, selected_routes_player2):
    """
    A function to run a simulation to compare given routes and say if there exists another route of equal length within another route.
    """
    intersecting_routes = []
    number_of_equivalent_nested_routes = 0
    for j in range(len(selected_routes_player2)):
            intersecting_routes.append(list(set(selected_route[0]).intersection(selected_routes_player2[j - 1])))
    for k in intersecting_routes:
        if len(k) == len(selected_route[0]):
            print(k)
            number_of_equivalent_nested_routes += 1
    return number_of_equivalent_nested_routes

def chances_of_knowing_which_long_route_player_has(given_long_route=Lisboa_Danzic, checking_length=2, BPL=False):
    """
    A function to check what the odds are of a player having a given long route by checking which other routes they could possibly have, 
    based on the length of the journey that they have completed so far.
    """
    blocks = 0
    if BPL == True:
        all_routes_excluding_given = short_routes + long_routes_BPL
    else:
        all_routes_excluding_given = short_routes + long_routes
    all_routes_excluding_given.remove(given_long_route)
    possible_combinations = itertools.combinations(given_long_route, r=checking_length + 1)
    for i in possible_combinations:
        blocks += number_of_equal_length_routes(selected_route=[list(i)], selected_routes_player2=all_routes_excluding_given)
    return 1 / (blocks + 1)

def completeing_blocking_attempt(number_of_remaining_pieces=20.8406495371769691, BPL=False, palermoconstantinople_kobenhavenerzurum=True):
    """
    A function to check how successful you are in blocking against your opponent. With completing short routes first, we expect each player 
    to have 20.8406495371769691 pieces remaining to complete their long route.
    We also consider whether or not we include Palermo-Constantinople and Kobenhaven-Erzurum, as they have such high blocking ability.
    """
    if palermoconstantinople_kobenhavenerzurum == True:
        long_routes_blocking_stats_BPN = [{"route": Lisboa_Danzic, "amount blocked": 14 + 17}, 
                                          {"route": Cadiz_Stockholm, "amount blocked": 15 + 24}, 
                                          {"route": Palermo_Moskva, "amount blocked": 45}, 
                                          {"route": Kobenhaven_Erzurum, "amount blocked": 13 + 33}, 
                                          {"route": Edinburgh_Athina, "amount blocked": 12 + 16}, 
                                          {"route": Brest_Petrograd_Normal, "amount blocked": 14 + 13}]
        long_routes_blocking_stats_BPL = [{"route": Lisboa_Danzic, "amount blocked": 14 + 17}, 
                                          {"route": Cadiz_Stockholm, "amount blocked": 15 + 24}, 
                                          {"route": Palermo_Moskva, "amount blocked": 45}, 
                                          {"route": Kobenhaven_Erzurum, "amount blocked": 13 + 33}, 
                                          {"route": Edinburgh_Athina, "amount blocked": 12 + 16}, 
                                          {"route": Brest_Petrograd_Long, "amount blocked": 17 + 11}]
    else:
        long_routes_blocking_stats_BPN = [{"route": Lisboa_Danzic, "amount blocked": 14 + 17}, 
                                          {"route": Cadiz_Stockholm, "amount blocked": 15 + 24}, 
                                          {"route": Edinburgh_Athina, "amount blocked": 12 + 16}, 
                                          {"route": Brest_Petrograd_Normal, "amount blocked": 14 + 13}]
        long_routes_blocking_stats_BPL = [{"route": Lisboa_Danzic, "amount blocked": 14 + 17}, 
                                          {"route": Cadiz_Stockholm, "amount blocked": 15 + 24}, 
                                          {"route": Edinburgh_Athina, "amount blocked": 12 + 16}, 
                                          {"route": Brest_Petrograd_Long, "amount blocked": 17 + 11}]
    
    if BPL == True:
        selected_long_route = random.sample(long_routes_blocking_stats_BPL, k=1)
    else:
        selected_long_route = random.sample(long_routes_blocking_stats_BPN, k=1)
    if random.random() <= 0.026463180638737385:
        rand_number = random.random()
        if selected_long_route[0]["route"] == Edinburgh_Athina:
            if rand_number <= 9 / 40:
                return True, 0
        if selected_long_route[0]["route"] == Kobenhaven_Erzurum:
            if rand_number <= 2 / 40:
                return True, 0
        if selected_long_route[0]["route"] == Cadiz_Stockholm:
            if rand_number <= 2 / 40:
                return True, 0
        if selected_long_route[0]["route"] == Lisboa_Danzic:
            number_of_remaining_pieces -= 5
        if selected_long_route[0]["route"] == Brest_Petrograd_Normal:
            if rand_number <= 7 /40:
                return True, 0
        if selected_long_route[0]["route"] == Brest_Petrograd_Long:
            if rand_number <= 8 / 40:
                return True, 0
    if number_of_remaining_pieces <= selected_long_route[0]["amount blocked"]:
        return True, 0
    else:
        return False, (number_of_remaining_pieces - selected_long_route[0]["amount blocked"])

def probability_blocking_opponent_from_completing_routes(repetitions=10_000, number_of_pieces=20.8406495371769691, BPL=False, 
                                                         palermoconstantinople_kobenhavenerzurum=True):
    """
    A function to run a large simulation to check what the chances are of completing all routes against a blocking opponent.
    """
    successes = 0
    sum_of_remaining_pieces = 0
    for i in range(repetitions):
        success_of_block, remaining_pieces = completeing_blocking_attempt(number_of_remaining_pieces=number_of_pieces, BPL=BPL, 
                                                                          palermoconstantinople_kobenhavenerzurum=palermoconstantinople_kobenhavenerzurum)
        sum_of_remaining_pieces += remaining_pieces
        if success_of_block == True:
            successes += 1
    return (successes / repetitions), (sum_of_remaining_pieces / repetitions)

def number_of_turns_for_ERB(selected_routes):
    """
    A function to check lengths of routes to find the number of turns that it takes to complete all routes. 
    """
    number_of_turns_required = 0
    for i in selected_routes:
        number_of_turns_required += len(i) - 1
    return number_of_turns_required

def average_number_of_turns_for_ERB_short(repetitions=1_000):
    """
    A function to run a large simulation to find the average number of turns it takes to place all track to complete short routes with ERB.
    """
    total_number_of_moves = 0
    for i in range(repetitions):
        selected_routes_player1, selected_routes_player2 = initial_short_route_selection(number_of_short_routes=3)
        total_number_of_moves += number_of_turns_for_ERB(selected_routes_player1)
    return (total_number_of_moves / (3 * repetitions))


# Below we have what was found by using the above code to find expectations and standard deviations:

#ERB vs ERB
expected_scores1 = [109.18, 110.34]
stds1 = [3.0363511240578847, 3.1611963377408534]

#ERB-NS vs Blocker
expected_scores2 = [91.25, 90.25]
stds2 = [1.55, 1.55]

#ERB-LS vs Blocker
expected_scores3 = [91.69, 91.42]
stds3 = [2.094450338924805, 1.4907119849998596]

#ERB-NL vs Blocker
expected_scores4 = [92.77, 93.46]
stds4 = [1.4283556979968264, 1.9139023544115896]

#ERB-LL vs Blocker
expected_scores5 = [93.70, 97.06]
stds5 = [2.083607981896361, 4.459486766683157]

#LT vs Blocker
expected_scores6 = [52.24, 44.73]
stds6 = [1.1736028928048874, 0.5]

#ERB-NS vs LT
expected_scores7 = [43.10, 54.09]
stds7 = [1.8103243647356568, 1.1055415967851332]

#ERB-LS vs LT
expected_scores8 = [46.77, 52.01]
stds8 = [4.27460199576782, 2.1392496088322392]

#ERB-NL vs LT
expected_scores9 = [56.20, 53.18]
stds9 = [4.645451236436021, 0.82915619758885]

#ERB-LL vs LT
expected_scores10 = [57.39, 52.59]
stds10 = [5.801167267599399, 2.034425935955617]

def find_probability_strategy_A_beats_strategy_B(strategyA_expected_score, StrategyB_expected_score, strategyA_std, strategyB_std):
    """
    A function to take given expected scores and standard deviations for our strategies and use that to find the probability that 
    strategy A beats strategy B.
    """
    z_score = (strategyA_expected_score - StrategyB_expected_score) / np.sqrt(strategyA_std ** 2 + strategyB_std ** 2)
    return stats.norm.ppf(z_score)


A = np.array(
    [
        [0.5, 0.396, 0.5, 0.396, 0.676, 0], 
        [0.604, 0.5, 0.604, 0.5, 0.542, 0.136], 
        [0.5, 0.396, 0.5, 0.396, 0.386, 0.739], 
        [0.604, 0.5, 0.604, 0.5, 0.247, 0.783], 
        [0.324, 0.458, 0.614, 0.753, 0.5, 0], 
        [1, 0.864, 0.261, 0.217, 1, 0.5]
        ]
        )

B = np.array(
    [
        [0.5, 0.604, 0.5, 0.604, 0.324, 1], 
        [0.396, 0.5, 0.396, 0.5, 0.458, 0.864], 
        [0.5, 0.604, 0.5, 0.604, 0.614, 0.261], 
        [0.396, 0.5, 0.396, 0.5, 0.753, 0.217], 
        [0.676, 0.542, 0.386, 0.247, 0.5, 1], 
        [0, 0.136, 0.739, 0.783, 0, 0.5]
        ]
        )

nash_equilibria = [
                   [0, 0, 0, 0.48262548, 0.27316602, 0.24420849], 
                   [0, 0, 0, 0.48262548, 0.27316602, 0.24420849]
                   ]

action_set = [i for i in range(216)]

def replicator_dynamics(game_matrix, iterations=1_000, intervals=1_000):
    """
    Uses nashpy replicator dynamics the interaction matrix to find which stratergies survive over time.
    """
    timepoints = np.linspace(0, iterations, intervals)
    game = nash.Game(game_matrix)
    replicator_game = game.replicator_dynamics(timepoints=timepoints)
    return replicator_game
    
def replicator_dynamics_graph(outcome_array, strat_names):
    """
    Using the replicator dynamics function from nashpy to show the population share of strategies over time.
    """
    x = np.linspace(0, len(outcome_array), len(outcome_array))
    y_vals = outcome_array
    y_vals = list(map(list, zip(*outcome_array)))
    fig, ax = plt.subplots()
    lines = []
    for line_index in range(0, len(y_vals)):
        lines.append(ax.plot(x, y_vals[line_index], label=strat_names[line_index]))
    ax.legend()
    ax.set_xlabel("games")
    ax.set_ylabel("population share")
    plt.show()

def repeat_game_once(A, B):
    """
    A function to use nested for loops to get the column and row player matrices for our game being repeated once with expected wins as the 
    entries instead of win rates.
    """
    A_rep1 = [[] for i in range(36)]
    for i in range(len(A)):
        for j in range(len(A)):
            for k in range(len(A[i])):
                for p in range(len(A[j])):
                    A_rep1[6 * i + j].append(round(A[i][j] + A[k][p], ndigits=3))

    B_rep1 = [[] for i in range(36)]
    for i in range(len(B)):
        for j in range(len(B)):
            for k in range(len(B[i])):
                for p in range(len(B[j])):
                    B_rep1[6 * i + j].append(round(B[i][j] + B[k][p], ndigits=3))
    game_rep1 = nash.Game(A_rep1, B_rep1)
    return A_rep1, B_rep1, game_rep1

def repeat_game_twice(A, B):
    """
    A function to use nested for loops to get the column and row player matrices for our game being repeated twice with expected wins as the 
    entries instead of win rates.
    """
    A_rep2 = [[] for i in range(216)]
    for i in range(len(A)):
        for j in range(len(A)):
            for k in range(len(A[i])):
                for p in range(len(A[j])):
                    for q in range(len(A[i])):
                        for m in range(len(A[j])):
                            A_rep2[36 * i + 6 * j + k].append(round(A[i][j] + A[k][p] + A[q][m], ndigits=3))

    B_rep2 = [[] for i in range(216)]
    for i in range(len(B)):
        for j in range(len(B)):
            for k in range(len(B[i])):
                for p in range(len(B[j])):
                    for q in range(len(B[i])):
                        for m in range(len(B[j])):
                            B_rep2[36 * i + 6 * j + k].append(round(B[i][j] + B[k][p] + B[q][m], ndigits=3))
    game_rep2 = nash.Game(A_rep2, B_rep2)
    return A_rep2, B_rep2, game_rep2

# Printing Lemke Howson nash eequilibria for our three games in a row:
repeated_A_twice, repeated_B_twice, game_repeated_twice = repeat_game_twice(A=A, B=B)
eqs = game_repeated_twice.lemke_howson(initial_dropped_label=2)
print(eqs)
# Graphing replicator dynamics for single game:
game_outcome = replicator_dynamics(game_matrix=A, iterations=500, intervals=500)
replicator_dynamics_graph(outcome_array=game_outcome, strat_names=action_set)