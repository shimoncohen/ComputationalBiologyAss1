from enum import IntEnum
import random
import numpy as np

class DoubtLevel(IntEnum):
    S1 = 0,
    S2 = 1,
    S3 = 2,
    S4 = 3

    @staticmethod
    def max():
        return max(list(DoubtLevel))

    @staticmethod
    def get_probability(doubt_level: int) -> float:
        size = len(DoubtLevel)
        intervals = np.linspace(0, 1, size)
        return intervals[doubt_level]

    @staticmethod
    def map_to_str(doubt_level: int) -> str:
        m = {
            DoubtLevel.S1: 'S1',
            DoubtLevel.S2: 'S2',
            DoubtLevel.S3: 'S3',
            DoubtLevel.S4: 'S4'
        }

        return m.get(doubt_level, '')

class Person:
    def __init__(self, doubt_level: DoubtLevel, cooldown_time: int) -> None:
        self.__doubt_level = doubt_level
        # Cooldown should take into account the next generation in which the rumor is passed
        self.__cooldown_time = cooldown_time + 1
        self.__cooldown = 0
        self.__has_been_affected = False
    
    @property
    def doubt_level(self):
        return self.__doubt_level
    
    @property
    def cooldown(self):
        return self.__cooldown
    
    @property
    def has_been_affected(self):
        return self.__has_been_affected

    def should_pass_rumor(self, num_neighbours: int) -> bool:
        p = random.uniform(0, 1)
        if num_neighbours == 0 or self.__cooldown > 0 or p == 1:
            return False

        doubt_level = self.__doubt_level
        if num_neighbours >= 2 and doubt_level > 0:
            doubt_level -= 1

        threshold = DoubtLevel.get_probability(doubt_level)
        return threshold <= p

    def activate_cooldown(self):
        self.__cooldown = self.__cooldown_time
        self.__has_been_affected = True

    def update_cooldown(self):
        if self.__cooldown > 0:
            self.__cooldown -= 1
