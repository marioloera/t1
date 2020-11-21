#!/usr/bin/env python3
import csv


class FlightPerCountry:

    def __init__(self, airports_by_iata):
        # TODO receive airports_by_id, airports_by_icao
        self.airports_by_iata = airports_by_iata
        self.countries = {}
        self.unknown_country = "unknown"
        # {country:[domestic_flight, international_flight]}
        self.countries[self.unknown_country] = [0, 0]

    def print_results(self):
        print('\nresults:')
        domesticAcc = 0
        internationalAcc = 0
        for country in sorted(self.countries.keys()):
            flights = self.countries[country]
            if sum(flights) > 0:
                domesticAcc += flights[0]
                internationalAcc += flights[1]
                print(country, flights[0], flights[1])
        print(domesticAcc + internationalAcc, domesticAcc, internationalAcc)

    def save_results(self, output_file):
        """
        outputs the number of domestic and international flights for 
        each country according to this format: 
        country,domestic_flights,international_flights, e.g.
            Austria,2380,1220
            [...]
            United Kingdom,12371,2899
            [...]
        """
        results = []
        for country in sorted(self.countries.keys()):
            flights = self.countries[country]
            domestic_flights = flights[0]
            international_flights = flights[1]
            results.append([country, domestic_flights, international_flights])

        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(results)
        except OSError as ex:
            print(ex)
            pass

    def process_flight(self, row):
        '''
        Procees each flight, get the airport countries
        and add domestic or international flight to the countries dictionary 
        fro the source country.
        unknown airport will be add to the unknown coutry record
        '''
        # get row info
        source_airport = row[2]
        source_airport_id = row[3]
        destination_airport = row[4]
        destination_airport_id = row[5]

        # get countrys
        source_country = self.get_airport_country(airport_code=source_airport)
        destination_coutry = self.get_airport_country(
            airport_code=destination_airport)

        # check if is domestic or international flight
        domestic_flight = 1
        international_flight = 0
        if (source_country != destination_coutry):
            domestic_flight = 0
            international_flight = 1

        # unknow destination will be add to unknow country count
        if destination_coutry == self.unknown_country:
            source_country = self.unknown_country

        # add country to countries dictionary
        if source_country not in self.countries:
            self.countries[source_country] = [0, 0]

        # add flights to countries
        self.countries[source_country][0] += domestic_flight
        self.countries[source_country][1] += international_flight

    def get_airport_country(self, airport_code=None, airport_id=None):
        '''
        return the country for airport.
        frist checking the ariport_code in the iata dictionary, 
        
        # TODO then airport_id in the airport id dictionary,
        # TODO last airport_code in the icao dictionary.
        if not found then return unknown_country variable.
        '''
        country = self.airports_by_iata.get(airport_code, self.unknown_country)
        return country
