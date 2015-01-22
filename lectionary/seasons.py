import sys

import _seasons

seasons = _seasons.Seasons(
    'Advent',
    'Christmas',
    'Epiphany',
    'Transfiguration',
    'Lent',
    'Easter',
    'Pentecost',
    'End Of Year',
    'Last Sunday'
)

seasons.__doc__ = __doc__
sys.modules[__name__] = seasons
