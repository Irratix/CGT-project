import sys
from itertools import permutations
from collections import Counter
import random

# generate all possible partial preference profiles for one agent
def generate_preferences(house_amt):
    return list(permutations(range(house_amt)))

# generate partial preference profile
def generate_preference(house_amt):
    return random.sample(range(house_amt), house_amt)

# generate preference profile
def generate_profile(agent_amt, house_amt):
    profile = []
    for agent in range(agent_amt):
        profile.append(generate_preference(house_amt))
    return profile

# calculate probability matrix using the probabilistic serial rule
def probability_matrix(profile):
    agent_amt = len(profile)
    house_amt = len(profile[0])
    # init data of how much of each house is remaining and who ate how much
    houses = [1] * house_amt
    agents = [[0] * house_amt for _ in range(agent_amt)]

    # probabilistic serial rule
    while max(houses) != 0:
        # for each player, find out which house they're eating
        houses_selected = [next(i for i in preference if houses[i] != 0) for preference in profile]

        # how long does it take to eat each house
        house_counts = Counter(houses_selected)
        total_rate_eaten = [house_counts.get(i, 0) for i in range(house_amt)]
        time_to_eat = [None if total_rate_eaten[i] == 0 else houses[i] / total_rate_eaten[i] # Condition to avoid division by zero
                 for i in range(house_amt)]

        # take the lowest time to eat and step forward that amount of time
        t = min(t for t in time_to_eat if t is not None) # poor second condition to avoid floating point errors
        for agent in range(agent_amt):
            house = houses_selected[agent]
            houses[house] -= t
            agents[agent][house] += t
        houses = [house if house > 1e-9 else 0 for house in houses] # 
    return agents

# calculate expected utilities from applying Borda scores of a profile to a probability matrix
# Borda score starts at 0
def expected_utilities(matrix, profile):
    agent_amt = len(profile)
    house_amt = len(profile[0])
    utilities = []
    for agent in range(agent_amt):
        utility = 0
        for house in range(house_amt):
            house_value = agent_amt - 1 - profile[agent].index(house)
            utility += matrix[agent][house] * house_value
        utilities.append(utility)
    return utilities

def main():
    agent_amt = int(sys.argv[1])
    house_amt = int(sys.argv[2])
    profile = generate_profile(agent_amt, house_amt)
    matrix = probability_matrix(profile)
    utilities = expected_utilities(matrix, profile)
    print(utilities)

if __name__ == "__main__":
    main()
