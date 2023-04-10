import pytest
from src.loader.board_file_handler import BoardFileHandler, BoardFileData


class TestBoardFileHandler:
    @pytest.mark.parametrize(
        "L, people, rumors, people_arr, rumors_arr",
        [
            pytest.param('10', '4', '1', [[4]], [[1]]),
            pytest.param(
                '10', '4444\n4444', '1111\n1111',
                [[4, 4, 4, 4],
                [4, 4, 4, 4]],
                [[1, 1, 1, 1],
                [1, 1, 1, 1]]
            ),
        ]
    )
    def test_read_data_correctly(self, fs_no_root, L, people, rumors, people_arr, rumors_arr):
        path = '/path/to/text.txt'
        fs_no_root.create_file(path, contents=f"""{L}\n\n{people}\n\n{rumors}\n\n""")
        board_data: BoardFileData = BoardFileHandler.read_data(path)

        assert board_data.cooldown == L

        assert len(board_data.people) == len(people_arr)
        assert len(board_data.people[0]) == len(people_arr[0])
        assert all([[p1 == p2 for p1, p2 in zip(arr1, arr2)] for arr1, arr2 in zip(board_data.people, people_arr)])

        assert len(board_data.rumor_board) == len(rumors_arr)
        assert len(board_data.rumor_board[0]) == len(rumors_arr[0])
        assert all([[r1 == r2 for r1, r2 in zip(arr1, arr2)] for arr1, arr2 in zip(board_data.rumor_board, rumors_arr)])
    
    @pytest.mark.parametrize(
        "L, people, rumors, err_msg",
        [
            pytest.param('', '4', '1', 'File does not contain all of the needed data: cooldown, people, rumors'),
            pytest.param('10', '', '1', 'File does not contain all of the needed data: cooldown, people, rumors'),
            pytest.param('10', '4', '', 'File does not contain all of the needed data: cooldown, people, rumors'),
            pytest.param('c', '4', '1', 'The value provided for cooldown should be a positive number'),
            pytest.param('-1', '4', '1', 'The value provided for cooldown should be a positive number'),
            pytest.param('10', '4444', '0121\n1101', 'people and rumors should be of the same dimensions'),
            pytest.param('10', '4444\n4444', '0121\n111', 'people or rumors are not a valid matrix'),
            pytest.param('10', '444\n4444', '1111\n1111', 'people or rumors are not a valid matrix'),
            pytest.param('10', '4044\n4454', '1111\n1111', 'people should be constructed only from numbers 0 to 4'),
            pytest.param('10', '4444\n4444', '0121\n1101', 'rumor should be constructed only from 0 or 1'),
        ]
    )
    def test_read_data_correctly(self, fs_no_root, L, people, rumors, err_msg):
        path = '/path/to/text.txt'
        fs_no_root.create_file(path, contents=f"""{L}\n\n{people}\n\n{rumors}\n\n""")
        with pytest.raises(Exception) as e:
            BoardFileHandler.read_data(path)
        
        assert err_msg in str(e.value)