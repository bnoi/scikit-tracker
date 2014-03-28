import numpy as np
from . import AbstractLinkCostFunction
from ...trajectories import Trajectories
            
class GCLinkCostFunction(AbstractLinkCostFunction):
    """Basic cost function.

    Parameters
    ----------
    context : dict
    parameters : dict
        Missing parameters will be filled by DEFAULT_PARAMETERS
    """

    def __init__(self, context, parameters):
        super().__init__(context, parameters)
        if not 'trajs' in context.keys():
            raise ValueError('''The class GCLinkCostFunction requires '''
                             '''the `context` dictionnary to contain a `trajs` key''')

        if not isinstance(context['trajs'], Trajectories):
            raise TypeError('''
                            `context['trajs']` should be a `Trajectories` instance
                            ''')
            
        self.trajs = context['trajs']
        
    def build(self):
        """
        """
        mat = np.empty((len(self.segments),
                        len(self.segments)))
        mat.fill(np.nan)
        return mat

