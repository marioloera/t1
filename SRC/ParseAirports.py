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

    aiports = get_airports(file_path=airports_file)
    # LAX: United States
    print(f"LAX: {aiports.get('LAX', '?')}")

    countryFlights = init_countries(aiports)
    print(f"Uruguay: {countryFlights['Uruguay']}")

    # proces flights
    flights_file = os.path.join(data_dir, 'routes.dat')

    flightPerCountry1 = FlightPerCountry(aiports, countryFlights, flights_file)


def get_airports(file_path):
    airportIdIndex = 4  # 0:AirportId, 4: IATA 5:ICAO
    countryIndex = 3
    aiports = {}

    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)

            for row in reader:
                # get the data per record
                country = row[countryIndex]
                airportId = row[airportIdIndex]
                aiports[airportId] = country

    except OSError as ex:
        print(ex)
        pass
    return aiports


def init_countries(airports_dic):
    countries = {}
    for airportId, country in airports_dic.items():
        if country not in countries:
            # domestic, internationals
            countries[country] = (0, 0)
    return countries


class FlightPerCountry:

    def __init__(self, aiports, countries, file_path):
        self.aiports = aiports
        self.countries = countries
        self.unkwonCountry = '?'
        self.get_flights_per_country(file_path)
        self.countries[self.unkwonCountry] = (0, 0)

    def get_flights_per_country(self, file_path):
        x = 0
        try:
            with open(file_path, 'r', encoding='UTF-8') as f:
                reader = csv.reader(f)

                for row in reader:
                    x += 1
                    self.process_flight(row)
                    if x == 10:
                        break
                    pass
        except OSError as ex:
            print(ex)
            pass

    def process_flight(self, row):

        sourceAirportIndex = 2
        destinationAirportIndex = 4
        sourceCountry = self.aiports.get(row[sourceAirportIndex], '?')
        destinationCoutry = self.aiports.get(row[destinationAirportIndex], '?')

        print(row, sourceCountry, '->', destinationCoutry)
        #if (sourceCountry == destinationCoutry):


if __name__ == '__main__':
    main()
    print('clean exit')
