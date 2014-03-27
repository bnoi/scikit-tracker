# import numpy as np

# from ...utils import print_progress

# from ..matrices import LinkBlock
# from ..matrices import DiagBlock
# from ..matrices import CostMatrix

# from ..cost_function import AbstractLinkCostFunction
# from ..cost_function import AbstractDiagCostFunction

# from ..cost_function import BrownianCostFunction
# from ..cost_function import DiagCostFunction

from . import AbstractSolver


class GapCloseSolver(AbstractSolver):
    """

    Parameters
    ----------
    trajs : pandas.DataFrame
    cost_functions : list of list
    """
    def __init__(self, trajs, cost_functions, coords=['x', 'y', 'z']):

        super().__init__(trajs)
