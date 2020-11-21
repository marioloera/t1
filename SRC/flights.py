#!/usr/bin/env python3
import os
import csv
from modules import airports
from modules import country_flights


def main():

    src_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(src_dir, '..', 'input_data')

    # proces airports
    airports_file = os.path.join(data_dir, 'airports.dat')
    airport1 = airports.Airport()
    process_airport_file(airports_file, airport1)

    # proces flights
    flights_file = os.path.join(data_dir, 'routes.dat')
    flight_per_country = country_flights.FlightPerCountry(
        airport1.airports_by_iata)
    process_flight_file(flights_file, flight_per_country)
    flight_per_country.print_results()


def process_airport_file(file_path, _airport):
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            for row in reader:
                _airport.process_airport_row(row)

    except OSError as ex:
        print(ex)
        pass


def process_flight_file(file_path, _flight_per_country):
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
                _flight_per_country.process_flight(row)
                x += 1
                if x == 70:
                    break
    except OSError as ex:
        print(ex)
        pass


if __name__ == '__main__':
    main()
    print('clean exit')
