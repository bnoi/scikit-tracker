from .trajectories import Trajectories
try:
    from . import draw
    __all__ = ['Trajectories', 'draw']

except ImportError:
    print('''Looks like matplotlib can't be imported,
          drawing won't be available ''')
    __all__ = ['Trajectories']
    
