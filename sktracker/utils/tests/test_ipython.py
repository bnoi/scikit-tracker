from nose.tools import with_setup

from sktracker.utils import in_ipython

def test_in_ipython():
    """Tests are supposed to be run outside an IPython process.
    """

    assert not in_ipython()
