
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from sktracker.utils import color
from sktracker.utils.color_system import CODE

def test_colors():
    for test_string in ["I am a test", ""]:
        for color_string in ['RED', 'YELLOW', 'PURPLE']:
            color_code = CODE[color_string]
            yield check_color, test_string, color_string, color_code

def check_color(test_string, color_string, color_code):
    colored_string = '\x1b[%im%s\x1b[0m' % (color_code, test_string)
    assert color(test_string, color_string) == colored_string
