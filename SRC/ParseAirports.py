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
    get_flights_per_country(country_dict=countryFlights, file_path=flights_file)

def get_airports(file_path):
    airportIdIndex = 4 # 0:AirportId, 4: IATA 5:ICAO 
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
    countries = {'?': (0, 0)}
    for airportId, country in airports_dic.items():
        if country not in countries:
            # domestic, internationals
            countries[country] = (0, 0)
    return countries

def get_flights_per_country(file_path, country_dict):

    
    x = 0
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)

            for row in reader:
                x += 1
                process_flight(row)
                if x == 10:
                    break
                pass
    except OSError as ex:
        print(ex)
        pass

def process_flight(row):
    print(row)
    sourceAirportIndex = 2
    sourceAirportIdIndex = 3
    destinationAirportIndex = 4
    destinationAirportIdIndex = 5

if __name__ == '__main__':
    main()
    print('clean exit')
