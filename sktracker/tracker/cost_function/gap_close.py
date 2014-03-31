from . import AbstractCostFunction
from ...trajectories import Trajectories

__all__ = ["AbstractGapCloseCostFunction"]


class AbstractGapCloseCostFunction(AbstractCostFunction):
    """
    """

    def __init__(self, context, parameters):
        """
        """
        super().__init__(context=context, parameters=parameters)

    def check_idxs_length(self):
        """Check wether idxs_in and idxs_out have the same length.
        """

        idxs_in = self.check_context('idxs_in', Trajectories)
        idxs_out = self.check_context('idxs_out', Trajectories)

        if not len(idxs_in) == len(idxs_out):
            raise ValueError('''self.context['idxs_in'] and self.context['idxs_out']
                             must have the same length ''')
