# FashionGames

**FashionGames** is a simulation of a graph-based game where each vertex (representing an individual) is either a "conformist" or a "rebel," and each individual can color themselves with one of two strategies (colors: 0 or 1). The objective of the game is to simulate and analyze the dynamics of how vertices (individuals) adjust their strategies based on their neighbors' strategies in a graph.

### How the Game Works:
- **Conformists**: These individuals prefer to be the same color as most of their neighbors. Their payoff is calculated as:
  - Payoff = (Number of neighbors with the same strategy) - (Number of neighbors with the opposite strategy).
  
- **Rebels**: These individuals prefer to differ from most of their neighbors. Their payoff is calculated as:
  - Payoff = (Number of neighbors with the opposite strategy) - (Number of neighbors with the same strategy).

The program simulates and analyzes the dynamics of this game, checking how each vertex adjusts its strategy based on the strategies of its neighbors.

### Features:
- Simulate how vertices (individuals) update their strategies over time based on their neighbors' strategies.
- Visualize the strategies and payoffs for each vertex in the graph.
- Analyze the evolution of strategies in various graph configurations.

### Brief project structure explanation:

In the `.main` file, you will find the code for the graphs referenced in my thesis.

The `fashion.py` file contains the definition of the `FashionGraph` class and its associated functions.

The `generowanie_wykresow` file includes code used to generate additional graphs for instances of the `FashionGraph` class.

The `niepotrzebne_funkcje` file contains code that was not ultimately used in the game analysis but could be useful for expanding the project or for conducting a deeper analysis of such games in the future.
