#!/usr/bin/env python3
import os
import csv
import logging
import argparse
from modules import airports
from modules import flights
from modules import country


def main():

    # go to src dir
    src_dir = os.path.dirname(os.path.realpath(__file__))

    # declare log file
    logging.basicConfig(
        filename=os.path.join(src_dir, 'log', 'flights.log'),
        format=
        '%(levelname)s: %(asctime)s: %(process)d: %(filename)s: %(funcName)s: %(message)s',
        level=logging.INFO,
    )
    logging.info(f'Process started!')

    # # output file
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file",
                        help="output file where results are stored")
    args = parser.parse_args()

    # input_data dir
    data_dir = os.path.join(src_dir, '..', 'input_data')

    # process airports
    airports_file = os.path.join(data_dir, 'airports.dat')
    airport1 = airports.Airport()
    process_airport_file(airports_file, airport1)

    # process flights
    flights_file = os.path.join(data_dir, 'routes.dat')
    flights1 = flights.Flights(airport1.airports_by_iata)
    country1 = country.Country()
    process_flight_file(flights_file, flights1, country1)

    # save results
    results = country1.get_results_format1()
    save_data(args.output_file, results)

    msg = f'Process completed!'
    logging.info(msg)
    print(msg)


def process_airport_file(file_path, _airport):
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            for row in reader:
                _airport.process_airport_row(row)

    except OSError as ex:
        logging.error(ex)
        raise


def process_flight_file(file_path, flights, country):
    '''
    process the csv data in the file
    and call the function flights.process_flight to get the source 
    and destianation countries,
    then call function country.add_flight(source_country, destinantion country)
    and will add to the country.countries
    '''
    x = 0 
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            for row in reader:
                source_country, destination_country = flights.get_countries(row)
                country.add_flight(source_country, destination_country)

    except OSError as ex:
        logging.error(ex)
        raise


def save_data(file_path, data):

    try:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    except OSError as ex:
        logging.error(ex)
        raise


if __name__ == '__main__':
    main()
