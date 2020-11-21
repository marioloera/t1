#!/usr/bin/env python3


class Airport:

    def __init__(self):
        # {airport_iata_code: country}
        self.airports_by_iata = {}
        self.airports_by_icao = {}
        self.airports_by_id = {}

    def process_airport_row(self, row):
        '''
        Procees each airport to get the country 
        and store in the airports dictionary
        '''
        # get row info
        id = row[0]
        country = row[3]
        iata = row[4]
        icao = row[5]
        self.airports_by_iata[iata] = country
        self.airports_by_icao[icao] = country
        self.airports_by_id[id] = country
