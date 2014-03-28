import numpy as np

class AbstractCostFunction:
    """Abstract class.

    Parameters
    ----------
    context : dict
    parameters : dict
        Missing parameters will be filled by DEFAULT_PARAMETERS
    """

    def __init__(self, context, parameters):
        self.context = context
        self.parameters = parameters

    def build(self):
        """
        """
        pass

    def check_columns(self, objects, cols):
        """Check pandas.DataFrame column names.

        Parameters
        ----------
        objects : list of pandas.DataFrame
        cols : list column names to check
        """
        cols_set = set(cols)
        for obj in objects:
            actual_cols_set = set(obj.columns.values)
            if not cols_set.issubset(actual_cols_set):
                raise ValueError("The passed dataframe doesn't"
                                 " contain the required columns."
                                 "Missing columns: {}".format(
                                     cols_set.difference(actual_cols_set)))
            
class AbstractLinkCostFunction(AbstractCostFunction):
    """Basic cost function.

    Parameters
    ----------
    context : dict
    parameters : dict
        Missing parameters will be filled by DEFAULT_PARAMETERS
    """

    def __init__(self, context, parameters):
        super().__init__(context, parameters)

    def build(self, objects_in, objects_out):
        """
        """
        mat = np.zeros((len(objects_in), len(objects_out)))
        return mat

class AbstractDiagCostFunction(AbstractCostFunction):
    """Basic cost function for diagonal block.

    Parameters
    ----------
    context : dict
    parameters : dict
        Missing parameters will be filled by DEFAULT_PARAMETERS
    """
    def __init__(self, context, parameters):
        super().__init__(context, parameters)

    def build(self, objects):
        """
        """
        vec = np.zeros(len(objects))
        return vec
