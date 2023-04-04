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

## Running the program

To run in CLI mode run:
>```python main.py```

To run in GUI mode run:
>```python graphics_main.py```

## Understanding the UI

WIP