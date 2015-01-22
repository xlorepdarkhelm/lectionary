import datetime

import seasons


class Historic(object):
    @property
    def _data(self):
        if not hasattr(self, '_Historic__data'):
            self.__data = {}

        return self.__data

    @_data.deleter
    def _data(self):
        if hasattr(self, '_Historic__data'):
            del self.__data

    @property
    def _date(self):
        if 'date' not in self._data:
            self._date = datetime.date.today()

        return self._data['date']

    @_date.setter
    def _date(self, value):
        if 'date' not in self._data or value != self._date:
            del self._data
            self._data['date'] = value

    @staticmethod
    def week_diff(date1, date2):
        if date1 > date2:
            raise ValueError(
                ' '.join([
                    "Cannot calculate difference in weeks for date ({date1})"
                    "which exists after it's comparing date ({date2})."
                ]).format(
                    date1=date1.strftime('%Y-%m-%d'),
                    date2=date2.strftime('%Y-%m-%d'),
                )
            )

        sunday1 = date1 - datetime.timedelta(days=date1.weekday())
        sunday2 = date2 - datetime.timedelta(days=date2.weekday())

        return int((sunday2 - sunday1).days / 7)

    @property
    def sunday(self):
        if 'sunday' not in self._data:
            self._data['sunday'] = \
                self._date - datetime.timedelta(self._date.weekday())
        return self._data['sunday']

    @property
    def christmas(self):
        if 'christmas' not in self._data:
            self._data['christmas'] = \
                datetime.date(self._date.year, 12, 25)
        return self._data['christmas']

    @property
    def advent(self):
        if 'advent' not in self._data:
            weekday = self.christmas.weekday()

            if weekday:
                advent = self.christmas - datetime.timedelta(
                    days=weekday,
                    weeks=3
                )
            else:
                advent = self.christmas - datetime.timedelta(weeks=4)

            self._data['advent'] = advent

        return self._data['advent']

    @property
    def last_sunday(self):
        if 'last_sunday' not in self._data:
            self._data['last_sunday'] = \
                self.advent - datetime.timedelta(weeks=1)
        return self._data['last_sunday']

    @property
    def end_of_year(self):
        if 'end_of_year' not in self._data:
            self._data['end_of_year'] = \
                self.last_sunday - datetime.timedelta(weeks=3)
        return self._data['end_of_year']

    @property
    def epiphany(self):
        if 'epiphany' not in self._data:
            self._data['epiphany'] = \
                datetime.date(self._date.year, 1, 6)
        return self._data['epiphany']

    @property
    def easter(self):
        if 'easter' not in self._data:
            a = self._date.year % 19
            b = int(self._date.year / 100)
            c = self._date.year % 100
            d = int(b / 4)
            e = b % 4
            f = int((b + 8) / 25)
            g = int((b - f + 1) / 3)
            h = int(19 * a + b - d - g + 15) % 30
            i = int(c / 4)
            k = c % 4
            l = (32 + 2 * e + 2 * i - h - k) % 7
            m = int((a + 11 * h + 22 * l) / 451)
            n = (h + l - 7 * m + 114)

            month = int(n / 31)
            day = n % 31 + 1

            self._data['easter'] = \
                datetime.date(self._date.year, month, day)
        return self._data['easter']

    @property
    def lent(self):
        if 'lent' not in self._data:
            self._data['lent'] = \
                self.easter - datetime.timedelta(weeks=5)
        return self._data['lent']

    @property
    def transfiguration(self):
        if 'transfiguration' not in self._data:
            self._data['transfiguration'] = \
                self.easter - datetime.timedelta(weeks=10)
        return self._data['transfiguration']

    @property
    def pentecost(self):
        if 'pentecost' not in self._data:
            self._data['pentecost'] = \
                self.easter + datetime.timedelta(weeks=7)
        return self._data['pentecost']

    @property
    def week(self):
        if 'week' not in self._data:
            # After Advent
            if self.sunday >= self.advent:
                week = self.week_diff(self.advent, self.sunday)

            # After Epiphany, Before Transfiguration
            elif (
                self.sunday >= self.epiphany
                and self.sunday < self.transfiguration
            ):
                week = self.week_diff(self.epiphany, self.sunday) + 5

            # Before Epiphany
            elif self.sunday < self.epiphany:
                week = 8 - self.week_diff(self.sunday, self.epiphany)

            # After Transfiguration, Before End of Church Year
            elif (
                self.sunday >= self.transfiguration
                and self.sunday < self.end_of_year
            ):
                week = self.week_diff(self.transfiguration, self.sunday) + 11

            # The End of the Church Year to Last Sunday (ie. Third Last - Last
            # or this could be reqritten for Michelmas)
            else:
                week = 58 - self.week_diff(self.sunday, self.last_sunday)

            self._data['week'] = week

        return self._data['week']

    @property
    def privileged(self):
        if 'privileged' not in self._data:
            self._data['privileged'] = not (
                self.week != 12 and (
                    self.sunday.strftime('%m-%d') in {
                        '12-24',
                        '12-25',
                        '12-26',
                        '12-27',
                        '12-28',
                        '01-06'
                    }
                    or (self.week > 7 and self.week < 16)
                    or (self.week > 30 and self.week < 57)
                )
            )
        return self._data['privileged']

    @property
    def season(self):
        if 'season' not in self._data:
            if self._date >= self.advent and self._date < self.christmas:
                season = seasons.advent

            elif self._date >= self.christmas or self._date < self.epiphany:
                season = seasons.christmas

            elif self._date == self.transfiguration:
                season = seasons.transfiguration

            elif self._date < self.lent:
                season = seasons.epiphany

            elif self._date < self.easter:
                season = seasons.lent

            elif self._date < self.pentecost:
                season = seasons.easter

            elif self._date < self.end_of_year:
                season = seasons.pentecost

            elif self._date == self.last_sunday:
                season = seasons.last_sunday

            else:
                season = seasons.end_of_year

            self._data['season'] = season

        return self._data['season']

    @property
    def season_week(self):
        if 'season_week' not in self._data:
            if self.season == seasons.advent:
                season_week = 1 + self.week_diff(self.advent, self._date)

            elif self.season == seasons.christmas:
                christmas_date = self.christmas
                if self.date < christmas_date:
                    christmas_date -= datetime.timedelta(years=1)

                season_week = 1 + self.week_diff(christmas_date, self._date)

            elif self.season == seasons.epiphany:
                season_week = 1 + self.week_diff(self.epiphany, self._date)

            elif self.season in {self.transfiguration, self.last_sunday}:
                season_week = 1

            elif self.season == self.lent:
                season_week = 1 + self.week_diff(self.lent, self._date)

            elif self.season == self.easter:
                season_week = 1 + self.week_diff(self.easter, self._date)

            elif self.season == self.pentecost:
                season_week = 1 + self.week_diff(self.pentecost, self._date)

            elif self.season == self.end_of_year:
                season_week = 1 + self.week_diff(self.end_of_year, self._date)

            self._data['season_week'] = season_week

        return self._data['season_week']


class ThreeYear(Historic):
    @property
    def transfiguration(self):
        if 'transfiguration' not in self._data:
            self._data['transfiguration'] = \
                self.easter - datetime.timedelta(weeks=7)
        return self._data['transfiguration']

    @property
    def privileged(self):
        if 'privileged' not in self._data:
            self._data['privileged'] = (
                self.week <= 7
                or (self.week > 15 and self.week < 22)
            )
        return self._data['privileged']

    @property
    def series(self):
        if 'series' not in self._data:
            year = self._date.year
            if self._date < self.advent:
                year -= 1

            self._data['series'] = ['A', 'B', 'C'][year % 3]

        return self._data['series']


class Michelmas(Historic):
    @property
    def end_of_year(self):
        if 'end_of_year' not in self._data:
            self._data['end_of_year'] = \
                self.last_sunday - datetime.timedelta(weeks=9)

        return self._data['end_of_year']
