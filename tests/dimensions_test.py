import pytest
from src.backend import dimensions

class TestDimensions:
    @pytest.mark.parametrize(
        "idxs,rows,cols,ans",
        [
            pytest.param(
                [[6, 6], [7, 3], [2, 8]], 5, 5, []
            ),
            pytest.param(
                [[0, 0], [7, 3]], 1, 1, [[0, 0]]
            ),
        ],
    )
    def test_clip(self, idxs, rows, cols, ans):
        assert dimensions.clip(idxs, rows, cols) == ans
    
    @pytest.mark.parametrize(
        "idxs,rows,cols,ans",
        [
            pytest.param(
                [[6, 6], [7, 3], [2, 8]], 5, 5, [[1, 1], [2, 3], [2, 3]]
            ),
            pytest.param(
                [[0, 0], [7, 3]], 1, 1, [[0, 0], [0, 0]]
            ),
        ],
    )
    def test_wrap(self, idxs, rows, cols, ans):
        assert dimensions.wrap(idxs, rows, cols) == ans