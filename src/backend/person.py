from enum import IntEnum
import random
import numpy as np

class DoubtLevel(IntEnum):
    S4 = 0,
    S3 = 1,
    S2 = 2,
    S1 = 3

    @staticmethod
    def get_probability(doubt_level: int) -> float:
        size = len(DoubtLevel)
        intervals = np.linspace(0, 1, size)
        return intervals[doubt_level]

class Person:
    def __init__(self, doubt_level: DoubtLevel, cooldown_time: int) -> None:
        self.__doubt_level = doubt_level
        self.__cooldown_time = cooldown_time
        self.__cooldown = 0
    
    @property
    def doubt_level(self):
        return self.__doubt_level

    def should_pass_rumor(self, num_neighbours: int) -> bool:
        p = random.uniform(0, 1)
        if num_neighbours == 0 or self.__cooldown > 0 or p == 0:
            return False

        doubt_level = self.__doubt_level
        if num_neighbours >= 2 and doubt_level > 0:
            doubt_level -= 1

        threshold = DoubtLevel.get_probability(doubt_level)
        return threshold >= p

    def activate_cooldown(self):
        self.cooldown = self.__cooldown_time

    def update_cooldown(self):
        if self.__cooldown > 0:
            self.__cooldown -= 1
