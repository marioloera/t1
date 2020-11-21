#!/usr/bin/env python3
import os
import csv


def main():

    src_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(src_dir, '..', 'input_data')

    print(f"src_dir: {src_dir}")
    print(f"data_dir: {data_dir}")

    # proces airports
    airports_file = os.path.join(data_dir, 'airports.dat')

    airports = get_airports(file_path=airports_file)
    # LAX: United States
    print(f"LAX: {airports.get('LAX', '?')}")

    countryFlights = init_countries(airports)
    print(f"Uruguay: {countryFlights['Uruguay']}")

    # proces flights
    flights_file = os.path.join(data_dir, 'routes.dat')

    flightPerCountry1 = FlightPerCountry(airports, flights_file)
    flightPerCountry1.print_results()


def get_airports(file_path):
    airport_id_index = 4  # 0:AirportId, 4: IATA, 5:ICAO
    country_index = 3
    airports = {}

    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)

            for row in reader:
                # get the data per record
                country = row[country_index]
                airport_id = row[airport_id_index]
                airports[airport_id] = country

    except OSError as ex:
        print(ex)
        pass
    return airports


def init_countries(airports_dic):
    countries = {}
    for airportId, country in airports_dic.items():
        if country not in countries:
            # country :[domestic, internationals]
            countries[country] = [0, 0]
    return countries


class FlightPerCountry:

    def __init__(self, airports, file_path):
        self.airports = airports
        self.countries = {}
        self.unknown_country = "unknown"
        # {country:[domestic_flight, international_flight]}
        self.countries[self.unknown_country] = [0, 0]

        self.get_flights_per_country(file_path)

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

    def get_flights_per_country(self, file_path):
        '''
        process the csv data in the file
        and call the funtion process_flight to get the 
        domistic and international flights for each country
        '''
        x = 0
        try:
            with open(file_path, 'r', encoding='UTF-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.process_flight(row)
                    # x += 1
                    # if x == 70:
                    #     break
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

        # add flights to countries
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
        then airport_id in the airport id dictionary,
        last airport_code in the icao dictionary.
        if not found then return unknown_country variable.
        '''
        country = self.airports.get(airport_code, self.unknown_country)
        return country


if __name__ == '__main__':
    main()
    print('clean exit')
