# Lab 9

## Introduction

The island model is a parallel variant of genetic algorithms designed to improve the exploration and exploitation capabilities of the optimization process. In the island model, the population is divided into multiple subpopulations, referred to as islands. Each island evolves independently, performing its own genetic algorithm operations such as selection, crossover, mutation, and replacement.

Periodically, individuals migrate between islands, allowing for the exchange of genetic information. This migration serves two main purposes:

Exploration: Migration enables the sharing of genetic material between islands, introducing diversity and preventing islands from converging too quickly to suboptimal solutions. This helps explore a broader solution space.

Exploitation: Islands can benefit from the improved individuals discovered on other islands. If a particular island finds a highly fit individual, this individual can spread to other islands during migration, contributing to the overall progress of the algorithm.

The migration process can be controlled by parameters such as migration frequency, the number of migrating individuals, and the selection criteria for migrants.

Overall, the island model aims to strike a balance between maintaining diversity within each subpopulation (island) and sharing successful solutions across different subpopulations. This parallelism can lead to more effective and efficient optimization, particularly in complex, multi-modal, or dynamic problem spaces.

## How it works

This script uses an island model approach where multiple populations evolve independently and exchange individuals periodically. The best individuals in each island and the global best individual are tracked throughout the evolution. The function returns the best individual found after the specified number of generations.


## Collaborations
I worked with: 
- Matteo Martini - s314786 (https://github.com/MatteMartini/Computational-Intelligence.git)