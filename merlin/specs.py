import cytoolz
import requests


def only(ubids, specs):
    """Filter specs on ubids.

    Args:
        ubids (seq): [ubid1, ubid3]
        specs (seq): [{spec1}, {spec2}, {spec3}, ...})

    Returns:
        tuple: [{spec1}, {spec3}]
    """

    return tuple(cytoolz.filter(lambda x: x['ubid'] in ubids, specs))


def mapped(ubids, specs):
    """Organizes specs by key.

    Args:
        ubids (dict): {'red':   ['ubid1', 'ubid2'], 
                       'green': ['ubid3', 'ubid4']}
        specs (seq):  [{spec1}, {spec2}, {spec3}, {spec4}]

    Returns:
        dict: {'red':   [spec1, spec2],
               'green': [spec3, spec4]}
    """
    
    return {k: only(v, specs) for k, v in ubids.items()}


def exist(ubids, specs):
    """Checks that all ubids are in the specs

    Args:
        ubids (seq): [ubid1, ubid2, ubid3, ...]
        specs (seq): [{spec1}, {spec2}, {spec3}]

    Returns:
        bool: True or False
    """

    return set(ubids).issubset(set(map(lambda x: x['ubid'], specs)))
    

def byubid(specs):
    """Organizes specs by ubid

    Args:
        specs (sequence): a sequence of chip specs

    Returns:
        dict: specs keyed by ubid
    """

    return {s['ubid']: s for s in specs}


def ubids(specs):
    """Extract ubids from a sequence of specs

    Args:
        specs (sequence): a sequence of spec dicts

    Returns:
        tuple: a sequence of ubids
    """

    return tuple(s['ubid'] for s in specs if 'ubid' in s)