import ast

__all__ = ["sanitize_dict", "guess_values_type"]


def sanitize_dict(obj):
    """Convert all dict values in str.

    Parameters
    ----------
    obj : dict

    Returns
    -------
    new_obj : dict with all values as str
    """

    new_obj = dict([(k, str(v)) for k, v in obj.items()])
    return new_obj


def guess_values_type(obj):
    """Try to convert dict values in various data type when possible.

    Parameters
    ----------
    obj : dict

    Returns
    -------
    new_obj : dict
    """

    casters = [ast.literal_eval, int, float]

    new_obj = {}
    for k, v in obj.items():
        _tmp = v
        for caster in casters:
            try:
                _tmp = caster(v)
            except:
                pass
        new_obj[k] = _tmp
    return new_obj
