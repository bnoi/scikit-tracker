from io import StringIO

from sktracker.utils import print_progress


def test_print_progress():
    out = StringIO()
    print_progress(15, out=out)
    output = out.getvalue().strip()
    bar = "15% [======>                                          ]"
    assert bar == output


def test_print_progress_remove_bar():
    out = StringIO()
    print_progress(-1, out=out)
    output = out.getvalue().strip()
    bar = ""
    assert bar == output
