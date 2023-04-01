from enum import Enum
from random import random

import numpy as np

class DoubtLevel(Enum):
    S4 = 0,
    S3 = 1,
    S2 = 2,
    S1 = 3

    def get_probability(doubt_level: int) -> float:
        size = len(DoubtLevel)
        intervals = np.linspace(0, 1, size)
        return intervals[doubt_level]

class Person:
    def __init__(self, doubt_level: DoubtLevel, cooldown_time: int) -> None:
        self.doubt_level = doubt_level
        self.cooldown_time = cooldown_time
        self.cooldown = 0

    def should_pass_rumor(self, num_neighbours: int) -> bool:
        doubt_level = self.doubt_level

        if num_neighbours >= 2:
            doubt_level -= 1
        
        p = random.uniform(0, 1)
        if p == 0:
            return False

        threshold = DoubtLevel.get_probability(doubt_level)
        return threshold >= p

    def _activate_cooldown(self):
        self.cooldown = self.cooldown_time

    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1
