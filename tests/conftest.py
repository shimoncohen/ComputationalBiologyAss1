import pytest
from pyfakefs.fake_filesystem_unittest import Patcher


@pytest.fixture()
def fs_no_root():
    with Patcher(allow_root_user=False) as patcher:
        yield patcher.fs