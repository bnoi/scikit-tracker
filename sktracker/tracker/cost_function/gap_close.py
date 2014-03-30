from . import AbstractLinkCostFunction
from ...trajectories import Trajectories

__all__ = ["AbstractGapCloseLinkCostFunction"]


class AbstractGapCloseLinkCostFunction(AbstractLinkCostFunction):
    """
    """

    def __init__(self, context, parameters):
        super().__init__(context, parameters)

        _parameters = {'distance_metric': 'euclidean',
                       'max_speed': 1.,
                       'coords': ['x', 'y', 'z']}
        _parameters.update(parameters)
        super().__init__({}, _parameters)
        self.context = context

    def update(self):
        """
        Updates the object's attributes according to context
        """
        self.trajs = self.context['trajs']
        # Just in case the parent didn't do it
        self.trajs.relabel_fromzero('label', inplace=True)

        self.idxs_in = self.context['idxs_in']
        self.idxs_out = self.context['idxs_out']
        if not len(self.idxs_in) == len(self.idxs_out):
            raise ValueError('''`self.context['idxs_in']` and `self.context['idxs_out']`
                             must have the same length ''')
        if 'trajs' not in self.context.keys():
            raise ValueError('''The class GCLinkCostFunction requires '''
                             '''the `self.context` dictionnary to contain a `trajs` key''')

        if not isinstance(self.context['trajs'], Trajectories):
            raise TypeError('''
                            `self.context['trajs']` should be a `Trajectories` instance
                            ''')
