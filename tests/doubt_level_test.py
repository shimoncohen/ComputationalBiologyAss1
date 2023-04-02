import pytest
import numpy as np
from src import person

class TestDoubtLevel:
    @pytest.mark.parametrize(
        "doubt_level",
        [
            pytest.param(person.DoubtLevel.S4),
            pytest.param(person.DoubtLevel.S3),
            pytest.param(person.DoubtLevel.S2),
            pytest.param(person.DoubtLevel.S1),
        ],
    )
    def test_should_pass_rumor_with_cooldown(self, doubt_level):
        size = len(person.DoubtLevel)
        intervals = np.linspace(0, 1, size)
        ans = intervals[doubt_level]
        assert person.DoubtLevel.get_probability(doubt_level) == ans