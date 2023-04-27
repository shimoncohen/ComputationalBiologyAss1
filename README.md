# ComputationalBiologyAss1
## What is this all about?
### The goal
Simulating passing rumors between a group of people in an $N \times M$ grid.\
The density of the population is determined by $P$, a parameter given by the user. This means that clusters of people could be formed (connectivity is not guarenteed).\
On the first generation (denote $g=0$) a random person is selected to start a rumor. Each person passes the rumor to his neighbours (8 or 4 depending on strategy). Each person decides if he believes the rumor depending on his type (Explained in the next section). If he decides to believe, the rumor is passes on in the next generation ($g + 1$).

### Types of people
There are four types of people:
- S1 - Believes everything he hears
- S2 - Believes something at probability $P = {2 \over 3}$
- S3 - Believes something at probability $P = {1 \over 3}$
- S4 - Doesn't believe anything

The percentage of each type in the population is a parameter decided by the user.

### Neighbour selecting strategies
Each person is affected by his neighbours. The definition of a person's neighbours is affected by two parameters:
- wrap_aroud - A boolean value decided by the user. Defines the existance of 'borders' at the edge of the board.
- neighbour selection strategy - The strategy is decided by the user and will be explained next.

Neighbor selection strategy types:
- ALL - All ehight adjacent cells
- CROSS - Top, Bottom, Left and Right neighbours
- DIAGONAL - Diagonal neighbours

## Setting up the environment
Python version should be 3.6 or above.

Install all of the requirements by running:
>```pip install -r requirements.txt```

## Setting up the program (CLI mode)
You may change the parameters in the `main.py` file.
There are a few versions to run:
- regular run with parameters
- load a board file for the simulation
- run all permutations for research

## Board file structure
First row is the L values, it should be zero or a positive number.
Line seperation.
Now should be the people board description. Each value represents a corresponding cell in the board. Valid values are:
- 0 (no person)
- one of 1,2,3,4 corresponding to wanted doubt level

Line seperation.
Now should be the rumor board description. Each value represents a corresponding cell in the board. Valid values are:
- 0 (no rumor)
- 1 (passing rumor)

Example for a valid board file:\
1

0000000\
0222220\
0222220\
0222220\
0222220\
0222220\
0000000

0000000\
0001000\
0001000\
0111110\
0001000\
0001000\
0000000

## Running the program
To run in CLI mode run:
>```python main.py```

To run in GUI mode run:
>```python graphics_main.py```
