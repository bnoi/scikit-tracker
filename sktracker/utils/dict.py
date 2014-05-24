__all__ = ["sanitize_dict", "guess_number_dict"]


def sanitize_dict(obj):
    """Convert all dict values in str.

    Parameters
    ----------
    obj : dict

    Return
    ------
    new_obj : dict with all values as str
    """
    new_obj = dict([(k, str(v)) for k, v in obj.items()])
    return new_obj


def guess_number_dict(obj):
    """Try to convert dict values in int and float when possible.

    Parameters
    ----------
    obj : dict

    Return
    ------
    new_obj : dict
    """
    new_obj = {}
    for k, v in obj.items():
        try:
            _tmp = int(v)
        except:
            try:
                _tmp = float(v)
            except:
                _tmp = v
        new_obj[k] = _tmp
    return new_obj
