import functools


@functools.total_ordering
class Season(object):
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def __str__(self):
        return "<{value}: {name}>".format(value=self.value, name=self.name)

    def __repr__(self):
        return "Season({name!r}, {value!r})".format(
            value=self.value,
            name=self.name
        )

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def __dir__(self):
        return ['name', 'value']

    def __dict__(self):
        return {
            'name': self.name,
            'value': self.value,
        }

    def __hash__(self):
        return hash((self.name, self.value))

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other


class Seasons(object):
    def __init__(self, *seasons):
        self.__seasons = tuple(
            Season(name, ndx)
            for ndx, name in enumerate(seasons)
        )

        for season in self.__seasons:
            setattr(self, season.name.lower().replace(' ', '_'), season)

    @property
    def __dict__(self):
        return {
            season.name.lower().replace(' ', '_'): season
            for season in self.__seasons
        }

    def __getitem__(self, value):
        return self.__seasons[value]

    def __call__(self, name):
        return getattr(self, name.lower().replace(' ', '_'))

    def __dir__(self):
        return [
            season.name.lower().replace(' ', '_')
            for season in self.__seasons
        ]

    def __iter__(self):
        return iter(self.__seasons)

    def __repr__(self):
        return ''.join([
            '<Seasons(',
            ', '.join([
                repr(season.name)
                for season in self.__seasons
            ]),
            ')>',
        ])
