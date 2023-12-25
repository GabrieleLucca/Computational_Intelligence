# Lab 10

## How it works

I am developing a player using the Q-learning algorithm to learn how to play a specific game. The goal is to enable the player to make intelligent decisions during the game, based on iteratively learned strategies. In my code, I have implemented a QPlayer class that manages Q-values, representing evaluations of state-action pairs. During the game, the player makes moves using an epsilon-greedy strategy, balancing exploration of new actions with exploitation of actions with higher evaluations. During training, Q-values are updated based on received rewards, allowing the player to progressively improve its decision-making. I am exploring and optimizing parameters such as the learning rate, discount factor, and exploration probability to maximize the player's performance in learning the game.
