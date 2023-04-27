# Ryan Dombroski
# CS 4100 Final Project

# Import statements
import random

# Creates a class to represent an MDP
class markovDecisionProcess:

    # Initializes the markovDecisionProcess
    # Name is the name as a string
    # Transition functions is a dictionary of tuples that represents the transition probabilities
    # Reward functions is also a dictionary of tuples that represents the reward probabilities
    # Nodes is a list of MarkovNodes in the MDP
    def __init__(self, name, transitionFunctions, rewardFunctions, nodes):
        self.name = name
        self.transitionFunctions = transitionFunctions
        self.rewardFunctions = rewardFunctions
        self.nodes = nodes

    # Outputs the results for value iteration for the given MDP
    def value_iteration(self, discountFactor, iterations):
        """
        Performs value iteration on the given MDP and prints the results
        The discount factor represents the discount factor variable
        Iterations represents the number of separate value iterations to perform
        """
        
        # Initialize our state variable, to keep track of what state we are currently in
        state_index = 0

        # Initialize the dictionary to keep track of the values for each state
        state_values = {}

        # While it is still in the specified iteration range
        while state_index < iterations:

            # The base state for 0
            if state_index == 0:
                
                # Iterate through nodes
                for node in self.nodes:

                    # Assign the value to zero for each node and iteration
                    state_values[(state_index, node.name)] = 0

            # Otherwise, if state is not 0
            else: 

                # Iterate through all of the nodes in the MDP
                for node in self.nodes:
                    # Get the name of the node/current state
                    state_name = node.name

                    # Keep track of the values for each possible actions
                    action_values = []

                    # Get value for current node
                    for action in node.actions.keys():

                        # Initialize the value for the value iteration equation
                        current_value = 0

                        # Iterate through the possible destinations for the action
                        for destination in node.actions[action]:

                            # Retrieve the transition and reward values for the current node
                            currentTransitionFunction = self.transitionFunctions[(state_name, action, destination)]
                            currentRewardFunction = self.rewardFunctions[(state_name, action, destination)]
                            previousValue = state_values[(state_index - 1, destination)]

                            # Calculate the value function using the above
                            current_value = current_value + (currentTransitionFunction * (currentRewardFunction + (discountFactor * previousValue)))

                        # Set the action values for the action that was just performed value iteration for
                        action_values.append(current_value)

                    # If length is 0
                    if len(action_values) == 0:
                        state_values[(state_index, state_name)] = 0
                    else:
                        state_values[(state_index, state_name)] = max(action_values)

            # Iterate through the state_index
            state_index += 1

        # Iterate through the values to print out to console
        for item in state_values:
            
            # Print out the result to console
            print("iteration: " + str(item[0]) + " state: " + str(item[1]) + " \n END VALUE: " + str(state_values[item]))



    # This function will randomly perform actions on the MDP, and output the score for each trial
    def play_mdp(self, iterations, starting_state, moves):
        """
        This function takes in the number of iterations to perform of the game
        It also specifies the starting state as a string
        And also specifies the number of moves for each iteration
        """

        # Initialize to keep track of the amount of iterations the game will play
        iterations_count = 0

        # Keep track of all of the final rewards
        reward_dict = {}

        # While the iterations count is below the iterations maximum
        while iterations_count < iterations:

            # How many moves of the game have been played
            move_count = 0

            # Initialize other starting variables
            new_starting = starting_state
            final_nodes = [starting_state]
            final_actions = []
            final_reward = 0

            # Make sure the game is below the specified iteration count
            while move_count < moves:
                initial_starting = new_starting
                # Iterate through the nodes to find the starting node
                for node in self.nodes:

                    # If the node is the starting state
                    if node.name == new_starting and node.name == initial_starting:
                        
                        # Choose an action at random from the current node
                        if not len(node.actions.keys()) == 0:
                            random_action = random.choice(list(node.actions.keys()))

                        # If there are not any possible actions at the node, then return
                        # Reached a terminal state
                        else: 
                            move_count += 1
                            break

                        # Get probability distribution for that action
                        random_choice = random.uniform(0, 1)

                        # Initialize the transition probability variable
                        # I will use this variable to help randomly select the result from an action
                        cumulativeTransitionProb = 0

                        # Add the action to the final actions list
                        final_actions.append(random_action)

                        # Iterate through the possible destinations
                        for destination in node.actions[random_action]:
                            
                            # Access the probability for the current action to the destination
                            currentTransitionProb = self.transitionFunctions[(node.name, random_action, destination)]

                            # If the current random is in the range of the current action/destination pair's transition probability, then
                            # Set as the final_destination
                            if random_choice >= cumulativeTransitionProb and random_choice < (currentTransitionProb + cumulativeTransitionProb):
                                final_nodes.append(destination)
                                final_reward = self.rewardFunctions[(node.name, random_action, destination)]
                                new_starting = destination


                            # Increase the cumulative probability
                            cumulativeTransitionProb = cumulativeTransitionProb + currentTransitionProb


                # Increment the move count
                move_count += 1


            # Return what nodes have been explored, what actions the game took, and the final reward
            reward_dict[final_reward] = reward_dict.get(final_reward, 0) + 1
            
            #return final_nodes, final_actions, final_reward
            iterations_count += 1

        print(reward_dict)

                    

# Creates a class to represent an node in an MDP
class markovNode:

    # Initializes the markovNode
    # Name is the name of the node
    # Actions is the possible actions, as a dictionary of action names, with possible destinations
    def __init__(self, name, actions):
        self.name = name
        self.actions = actions



# Creates examples for BlackJack
node_less21 = markovNode("<21", {"take": ["=21", "<21", ">21"], "not take": ["<21"]})
node_equal21 = markovNode("=21", {})
node_greater21 = markovNode(">21", {})

# =21 node v2, for the second version of blackjack
node_equal21_v2 = markovNode("=21", {"take": ["=32", "!=32"], "not take": ["=21"]})
node_equal32 = markovNode("=32", {})
node_notequal32 = markovNode("!=32", {})

# Nodes for the dice game
dice_different = markovNode("different", {"roll": ["different", "same", "two", "three"], "not roll": ["different"]})
dice_two = markovNode("two", {"roll": ["different", "two", "three"], "not roll": ["two"]})
dice_three = markovNode("three", {})
dice_same = markovNode("same", {})

# Creates transition functions for blackjack
blackjackTransition = {("<21", "take", "<21"): 0.0833, 
                       ("<21", "take", "=21"): 0.0833,
                       ("<21", "take", ">21"): 0.8334,
                       ("<21", "not take", "<21"): 1}

# Creates transition functions for the adapted version of blackjack
blackjackTransition_v2 = {("<21", "take", "<21"): 0.0833, 
                       ("<21", "take", "=21"): 0.0833,
                       ("<21", "take", ">21"): 0.8334,
                       ("<21", "not take", "<21"): 1,
                       ("=21", "not take", "=21"): 1,
                       ("=21", "take", "=32"): 0.0851,
                       ("=21", "take", "!=32"): 0.9149}

# Creates transition functions for the dice game
diceTransition = {("different", "roll", "different"): (191/216),
                  ("different", "roll", "three"): (6/216),
                  ("different", "roll", "two"): (18/216),
                  ("different", "roll", "same"): (1/216),
                  ("different", "not roll", "different"): 1,
                  ("two", "not roll", "two"): 1,
                  ("two", "roll", "three"): (6/216),
                  ("two", "roll", "two"): (18/216),
                  ("two", "roll", "different"): (192/216)}

# Creates reward functions for blackjack
blackjackRewards = {("<21", "take", "<21"): 1,
                    ("<21", "take", "=21"): 100,
                    ("<21", "take", ">21"): -1,
                    ("<21", "not take", "<21"): 0}

# Creates reward funcitons for the adapted version of blackjack
blackjackRewards_v2 = {("<21", "take", "<21"): 1,
                    ("<21", "take", "=21"): 100,
                    ("<21", "take", ">21"): -1,
                    ("<21", "not take", "<21"): 0,
                    ("=21", "not take", "=21"): 100,
                    ("=21", "take", "=32"): 200,
                    ("=21", "take", "!=32"): 50}

# Creates reward functions for the dice game
diceRewards = {("different", "roll", "different"): -1,
                  ("different", "roll", "three"): 1000,
                  ("different", "roll", "two"): 900,
                  ("different", "roll", "same"): 10000,
                  ("different", "not roll", "different"): 0,
                  ("two", "not roll", "two"): 10,
                  ("two", "roll", "three"): 1000,
                  ("two", "roll", "two"): 900,
                  ("two", "roll", "different"): 0}

# Create blackjack game as an MDP
blackjack = markovDecisionProcess("Blackjack", blackjackTransition, blackjackRewards, [node_less21, node_equal21, node_greater21])

# Print values and output for value iteration and different moves
print("Blackjack version 1, value iteration, discount factor 1, original values")
blackjack.value_iteration(1, 5)

print("\nBlakjack version 1, 1 move")
print(blackjack.play_mdp(10000, "<21", 1))

print("\nBlakjack version 1, 2 moves")
print(blackjack.play_mdp(10000, "<21", 2))

print("\nBlakjack version 1, 3 moves")
print(blackjack.play_mdp(10000, "<21", 3))


# Create second version of blackjack game as an MDP
blackjack_v2 = markovDecisionProcess("Blackjack_v2", blackjackTransition_v2, blackjackRewards_v2, [node_less21, node_equal21_v2, node_greater21, node_equal32, node_notequal32])

# Print values and output for value iteration and different moves
print("\n\nBlackjack version 2, value iteration, discount factor 1, original values")
blackjack_v2.value_iteration(1, 5)

print("\nBlakjack version 2, 2 moves")
print(blackjack_v2.play_mdp(10000, "<21", 2))

print("\nBlakjack version 2, 3 moves")
print(blackjack_v2.play_mdp(10000, "<21", 3))

print("\nBlakjack version 2, 4 moves")
print(blackjack_v2.play_mdp(10000, "<21", 4))

print("\nBlakjack version 2, 5 moves")
print(blackjack_v2.play_mdp(10000, "<21", 5))


# Create dice game as an MDP
dice_game = markovDecisionProcess("Dice_game", diceTransition, diceRewards, [dice_different, dice_two, dice_three, dice_same])

# Print values and output for value iteration and different numbers of moves
print("\n\nDice game, value iteration, discount factor 1, original values")
dice_game.value_iteration(1, 5)

print("\nDice game, 2 moves")
print(dice_game.play_mdp(10000, "different", 2))

print("\nDice game, 3 moves")
print(dice_game.play_mdp(10000, "different", 3))

print("\nDice game, 4 moves")
print(dice_game.play_mdp(10000, "different", 4))

print("\nDice game, 5 moves")
print(dice_game.play_mdp(10000, "different", 5))



