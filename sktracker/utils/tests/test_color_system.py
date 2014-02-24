from sktracker.utils import color
from sktracker.utils.color_system import CODE

def test_colors():
    for test_string in ["test", "test_string", "i am a test", ""]:
        for color_string, color_code in CODE.items():
            yield check_color, test_string, color_string, color_code

def check_color(test_string, color_string, color_code):
    colored_string = '\x1b[%im%s\x1b[0m' % (color_code, test_string)
    assert color(test_string, color_string) == colored_string
