#!/usr/bin/env python3
import logging


class AirportColumns:

    airport_id = 0
    name = 1
    city = 2
    country = 3
    iata = 4
    icao = 5
    latitude = 6
    longitude = 7
    altitude = 8
    timezone = 9
    dst = 10
    tz_db_time_zone = 11
    type = 12
    source = 13


class Airport:
    def __init__(self):
        # {airport_iata_code: country}
        self.airports_by_iata = {}
        self.airports_by_icao = {}
        self.airports_by_id = {}
        self.airport_col = AirportColumns()

    def process_airport_row(self, row):
        """
        Process each airport to get the country
        and store in the airports dictionary
        """
        # get row info
        try:
            id = row[self.airport_col.airport_id]
            country = row[self.airport_col.country]
            iata = row[self.airport_col.iata]
            icao = row[self.airport_col.icao]
            self.airports_by_iata[iata] = country
            self.airports_by_icao[icao] = country
            self.airports_by_id[id] = country

        except Exception as ex:
            msg = f"{ex}. row: {row}"
            logging.warning(msg)
            pass
