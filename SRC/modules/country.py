#!/usr/bin/env python3
import logging


class Country:

    def __init__(self):
        self.countries = {}
        self.unknown_country = "unknown"
        # {country:[domestic_flight, international_flight]}
        self.countries[self.unknown_country] = [0, 0]

    def get_results_format1(self):
        """
        return a list of list:
        [[country, domestic flights, international_fligthts],]
        in alphabetical order
        """
        results = [[c, self.countries[c][0], self.countries[c][1]]
                   for c in sorted(self.countries.keys())]

        return results

    def add_flight(self, source_country, destination_country):
        '''
            add to dic countries the domestic and internation flight increment
        '''
        try:

            # check if is domestic or international flight
            domestic_flight = 1
            international_flight = 0
            if (source_country != destination_country):
                domestic_flight = 0
                international_flight = 1

            # unknown destination will be added to unknown country count
            if destination_country == self.unknown_country:
                source_country = self.unknown_country

            # add country to countries dictionary
            if source_country not in self.countries:
                self.countries[source_country] = [0, 0]

            # add flights to countries
            self.countries[source_country][0] += domestic_flight
            self.countries[source_country][1] += international_flight

        except Exception as ex:
            logging.warning(ex)
            raise
