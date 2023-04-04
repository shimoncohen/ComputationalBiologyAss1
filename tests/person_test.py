import pytest
from src.backend.person import Person, DoubtLevel

class TestPerson:
    def test_activate_cooldown(self):
        p = Person(DoubtLevel.S1, 1)
        assert p.cooldown == 0

        p.activate_cooldown()
        assert p.cooldown > 0

    @pytest.mark.parametrize(
        "cooldown",
        [
            pytest.param(5),
            pytest.param(3),
            pytest.param(12),
        ],
    )
    def test_update_cooldown(self, cooldown):
        p = Person(DoubtLevel.S1, cooldown)
        assert p.cooldown == 0
        
        p.activate_cooldown()
        for _ in range(cooldown):
            assert p.cooldown > 0
            p.update_cooldown()

    @pytest.mark.parametrize(
        "doubt_level,cooldown,num_neighbours,ans_after_cooldown",
        [
            pytest.param(
                DoubtLevel.S1, 10, 1, True
            ),
            pytest.param(
                DoubtLevel.S3, 5, 2, False
            ),
            pytest.param(
                DoubtLevel.S4, 7, 1, False
            ),
        ],
    )
    def test_should_pass_rumor_with_cooldown(self, doubt_level, cooldown, num_neighbours, ans_after_cooldown):
        p = Person(doubt_level, cooldown)
        p.activate_cooldown()

        for _ in range(cooldown):
            assert p.should_pass_rumor(num_neighbours) == False
            p.update_cooldown()
        assert p.should_pass_rumor(num_neighbours) == ans_after_cooldown
    
    @pytest.mark.parametrize(
        "doubt_level,num_neighbours,ans",
        [
            pytest.param(
                DoubtLevel.S1, 1, True
            ),
            pytest.param(
                DoubtLevel.S3, 5, False
            ),
            pytest.param(
                DoubtLevel.S4, 8, False
            ),
        ],
    )
    def test_should_pass_rumor(self, doubt_level, num_neighbours, ans):
        p = Person(doubt_level, 0)
        assert p.should_pass_rumor(num_neighbours) == ans