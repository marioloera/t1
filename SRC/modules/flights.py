#!/usr/bin/env python3
import logging


class FlightColumns:

    airline = 0
    airline_id = 1
    source_airport = 2
    source_airport_id = 3
    destination_airport = 4
    destination_airport_id = 5
    codeshare = 6
    stops = 7
    equipment = 8


class Flights:
    def __init__(self, airports_by_iata):
        # TODO add arguments airports_by_id and airports_by_icao dictionaries
        self.airports_by_iata = airports_by_iata
        self.flight_col = FlightColumns()
        self.unknown_country = "unknown"

    def get_countries(self, row):
        """
        Process each flight, get the source and destination countries
        The flights where the source or destination airports are
        missing in airports_by_iata dictionary will be added
        to the unknown country record
        """
        # get row info
        try:
            source_airport = row[self.flight_col.source_airport]
            destination_airport = row[self.flight_col.destination_airport]

            # get countries
            source_country = self.get_airport_country(
                airport_code=source_airport
            )
            destination_country = self.get_airport_country(
                airport_code=destination_airport
            )

            return [source_country, destination_country]

        except Exception as ex:
            msg = f"{ex}. row: {row}"
            logging.warning(msg)
            pass

    def get_airport_country(self, airport_code=None, airport_id=None):
        country = self.airports_by_iata.get(airport_code, self.unknown_country)
        return country
