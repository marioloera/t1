#!/usr/bin/env python3
import os
import csv
import logging
import argparse
import pandas as pd

def main():

    # go to src dir
    src_dir = os.path.dirname(os.path.realpath(__file__))

    # declare log file
    # logging.basicConfig(
    #     filename=os.path.join(src_dir, 'log', 'flights.log'),
    #     format=
    #     '%(levelname)s: %(asctime)s: %(process)d: %(filename)s: %(funcName)s: %(message)s',
    #     level=logging.INFO,
    # )
    # logging.info(f'Process started!')

    # # output file
    # parser = argparse.ArgumentParser()
    # parser.add_argument("output_file",
    #                     help="output file where results are stored")
    # args = parser.parse_args()

    # input_data dir
    data_dir = os.path.join(src_dir, '..', 'input_data')
    airports_file = os.path.join(data_dir, 'airports.dat')
    flights_file = os.path.join(data_dir, 'routes.dat')

    # create dataframes from csv input files
    #airports_df = pd.read_csv(airports_file, header=False)
    airports_df = pd.read_csv(airports_file)

    # fligths_df = pd.read_csv(flights_file, header=False)
    # print(airports_df)
    # print(fligths_df)

    print(airports_df[0:5])



    # process airports

    msg = f'Process completed!'
    # logging.info(msg)
    print(msg)


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
