#!/usr/bin/env python3
import argparse
import csv
import logging
import os

from modules import airports, country_flights


def main():

    # go to src dir
    src_dir = os.path.dirname(os.path.realpath(__file__))

    # declare log file
    logging.basicConfig(
        filename=os.path.join(src_dir, "log", "flights.log"),
        format="%(levelname)s: %(asctime)s: %(process)d: %(filename)s: %(funcName)s: %(message)s",
        level=logging.INFO,
    )
    logging.info(f"Process started!")

    # output file
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_file", help="output file where results are stored"
    )
    args = parser.parse_args()

    # input_data dir
    data_dir = os.path.join(src_dir, "..", "input_data")

    # process airports
    airports_file = os.path.join(data_dir, "airports.dat")
    airport1 = airports.Airport()
    process_airport_file(airports_file, airport1)

    # process flights
    flights_file = os.path.join(data_dir, "routes.dat")
    flight_per_country = country_flights.FlightPerCountry(
        airport1.airports_by_iata
    )
    process_flight_file(flights_file, flight_per_country)

    # save results
    results = flight_per_country.get_results_format1()
    save_data(args.output_file, results)

    msg = f"Process completed!"
    logging.info(msg)
    print(msg)


def process_airport_file(file_path, _airport):
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                _airport.process_airport_row(row)

    except OSError as ex:
        logging.error(ex)
        raise


def process_flight_file(file_path, _flight_per_country):
    """
    process the csv data in the file
    and call the function process_flight to get the
    domestic and international flights for each country
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                _flight_per_country.process_flight(row)

    except OSError as ex:
        logging.error(ex)
        raise


def save_data(file_path, data):

    try:
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    except OSError as ex:
        logging.error(ex)
        raise


if __name__ == "__main__":
    main()
