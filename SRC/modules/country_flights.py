#!/usr/bin/env python3
import logging


class RoutesColumns:
    airline = 0
    airline_id = 1
    source_airport = 2
    source_airport_id = 3
    destination_airport = 4
    destination_airport_id = 5
    codeshare = 6
    stops = 7
    equipment = 8


class FlightPerCountry:
    def __init__(self, airports_by_iata):
        # TODO add arguments airports_by_id and airports_by_icao dictionaries
        self.airports_by_iata = airports_by_iata
        self.countries = {}
        self.unknown_country = "unknown"
        # {country:[domestic_flight, international_flight]}
        self.countries[self.unknown_country] = [0, 0]
        self.routes_col = RoutesColumns()

    def get_results_format1(self):
        """
        return a list of list:
        [[country, domestic flights, international_fligthts],]
        in alphabetical order
        """
        results = [
            [c, self.countries[c][0], self.countries[c][1]]
            for c in sorted(self.countries.keys())
        ]

        return results

    def process_flight(self, row):
        """
        Process each flight, get the airport countries
        and add the number of domestic and international flights to the countries dictionary
        from the source country.
        The flights where the source or destination airports are
        missing in airports_by_iata dictionary will be added to the unknown country record
        """
        # get row info
        try:
            source_airport = row[self.routes_col.source_airport]
            destination_airport = row[self.routes_col.destination_airport]
            # source_airport_id = row[self.routes_col.source_airport_id]
            # destination_airport_id = row[self.routes_col.destination_airport_id]

            # get countries
            source_country = self.get_airport_country(
                airport_code=source_airport
            )
            destination_country = self.get_airport_country(
                airport_code=destination_airport
            )

            # check if is domestic or international flight
            domestic_flight = 1
            international_flight = 0
            if source_country != destination_country:
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
            msg = f"{ex}. row: {row}"
            logging.warning(msg)
            pass

    def get_airport_country(self, airport_code=None, airport_id=None):
        """
        Return the country for the airport
        by checking the airport_code in the iata dictionary,
        if not found then return unknown_country variable.
        """
        country = self.airports_by_iata.get(airport_code, self.unknown_country)
        """
        TODO Test: when IATA code not found:
            use airport_id in the airport id dictionary
            or use airport_code in the ICAO dictionary.

        if country == self.unknown_country:
            country = self.airports_by_id.get(airport_id, self.unknown_country)

            if country == self.unknown_country:
                country = self.airports_by_icao.get(airport_code, self.unknown_country)
        """
        return country
