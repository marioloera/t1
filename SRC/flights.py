#!/usr/bin/env python3
import os
import csv
from modules import proces_flights


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

    # proces flights
    flights_file = os.path.join(data_dir, 'routes.dat')
    flight_per_country = proces_flights.FlightPerCountry(airports)
    process_flight_file(flights_file, flight_per_country)
    flight_per_country.print_results()


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


def process_flight_file(file_path, flight_per_ountry):
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
                flight_per_ountry.process_flight(row)
                x += 1
                if x == 70:
                    break
    except OSError as ex:
        print(ex)
        pass


if __name__ == '__main__':
    main()
    print('clean exit')
