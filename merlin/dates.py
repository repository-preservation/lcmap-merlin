from cytoolz import first
from cytoolz import reduce
from cytoolz import second
from cytoolz import thread_first
from dateutil import parser
from merlin import chips
from merlin import functions as f
import re


def to_ordinal(datestring):
    """Extract an ordinal date from a date string

    Args:
        datestring (str): date value

    Returns:
        int: ordinal date
    """

    return parser.parse(datestring).toordinal()


def startdate(acquired):
    """Returns the startdate from an acquired date string

    Args:
        acquired (str): / separated date range in iso8601 format

    Returns:
        str: Start date
    """

    return acquired.split('/')[0]


def enddate(acquired):
    """Returns the enddate from an acquired date string

    Args:
        acquired (str): / separated date range in iso8601 format

    Returns:
        str: End date
    """

    return acquired.split('/')[1]


def is_acquired(acquired):
    """Is the date string a / separated date range in iso8601 format?

    Args:
        acquired: A date string

    Returns:
        bool: True or False
    """

    # 1980-01-01/2015-12-31
    regex = '^[0-9]{4}-[0-9]{2}-[0-9]{2}\/[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    return bool(re.match(regex, acquired))


def mapped(chipmap):
    """Transform a dict of chips into a dict of datestrings

    Args:
        chipmap (dict): {k: [chips]}

    Returns:
        dict:  {k: [datestring2, datestring1, datestring3]}
    """

    return {k: chips.dates(v) for k, v in chipmap.items()}


def symmetric(datemap):
    """Returns a sequence of dates that are common to all map values if
    all datemap values are represented, else Exception.
    
    Args:
        datemap: {key: [datestrings,]}

    Returns:
        Sequence of date strings or Exception

    Example:

        >>> symmetric({"reds":  [ds3, ds1, ds2],
                       "blues": [ds2, ds3, ds1]})
        [ds2, ds3, ds1]
        >>>
        >>> symmetric({"reds":  [ds3, ds1],
                       "blues": [ds2, ds3, ds1]})
        Exception: assymetric dates detected - {'reds':[ds3, ds1]} != {'blues':[ds2, ds3, ds1]}
    """

    def check(a, b):
        """Reducer for efficiently comparing two unordered sequences.
        Executes in linear(On) time.

        Args:
            a: {k:[datestring1, datestring2...]}
            b: {k:[datestring2, datestring1...]}

        Returns:
            b if a == b, else Exception with details
        """

        if f.seqeq(second(a), second(b)):
            return b
        else:
            msg = ('assymetric dates detected - {} != {}'
                   .format(first(a), first(b)))
            msga = '{}{}'.format(first(a), second(a))
            msgb = '{}{}'.format(first(b), second(b))
            raise Exception('\n\n'.join([msg, msga, msgb]))

    return second(reduce(check, datemap.items()))


def symmetric_single(datemap):
    """Ensures all datemap values are length 1 & returns an iso8601 date range from the 
       min and max dates in datemap.values()

       Raises exception if values are not length 1.

    Args:
        datemap: {key: [datestrings,], key2: [datestrings,]}

    Returns:
        ['min_datestring/max_datestring',] or Exception

    Example:

        >>> symmetric({"nlcd": [ds3,],
                       "dem":  [ds2,]})
        [ds2/ds3,]
        >>>
        >>> symmetric({"nlcd":  [ds3, ds1],
                       "dem":   [ds2,]})
        Exception: assymetric dates detected - {'nlcd':[ds3, ds1], 'dem':[ds2]}
    """
    
    if all(map(lambda a: eq(1, len(a)), datemap.values())):
        return thread_first(datemap.values(),
                            f.flatten,
                            list,
                            lambda a: '{}/{}'.format(min(a), max(a)),
                            lambda a: [a,])
    else:
        raise Exception('assymetric dates detected - {}'.format(datemap))
    
    
def rsort(dateseq):
    """ Reverse sorts a sequence of dates.

    Args:
        dateseq: sequence of dates

    Returns:
        sequence: reverse sorted sequence of dates
    """
    
    return f.rsort(dateseq)
