#!/usr/bin/env python3
import os
import csv
import logging
import argparse
import pandas as pd
from modules import airports
from modules import flights


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

    # output file
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file",
                        help="output file where results are stored")
    args = parser.parse_args()

    # input_data dir
    data_dir = os.path.join(src_dir, '..', 'input_data')
    airports_file = os.path.join(data_dir, 'airports.dat')
    flights_file = os.path.join(data_dir, 'routes.dat')

    # airport & flights columns class
    airports_col = airports.AirportColumns()
    flights_col = flights.FlightsColumns()

    # create dataframes from csv input files
    airports_df_all = pd.read_csv(airports_file, names=airports_col.__list__)
    flights_df_all = pd.read_csv(flights_file, names=flights_col.__list__)

    # remove columns not needed so the join contains less columns
    # flights_df = flights_df_all.iloc[9:15, [
    flights_df = flights_df_all.iloc[:, [
        flights_col.source_airport,
        flights_col.destination_airport,
    ]]

    airports_df = airports_df_all.iloc[:, [
        airports_col.iata,
        airports_col.country,
    ]]

    # pands merge flights.source_airport airport.iata to get country
    src1 = flights_df.merge(airports_df,
                            left_on='source_airport',
                            right_on='iata')

    # pands merge src1 = flights.destination_airport airport.iata to get country
    # need to add suffixes becouse repeting columns names from airport
    src2 = src1.merge(airports_df,
                      left_on='destination_airport',
                      right_on='iata',
                      suffixes=('_src', '_dest'))

    # get domestic and international columns
    fn_domestic = lambda row: 1 if row.country_src == row.country_dest else 0
    fn_international = lambda row: 1 if row.country_src != row.country_dest else 0
    src2['domestic'] = src2.apply(fn_domestic, axis=1)
    src2['international'] = src2.apply(fn_international, axis=1)

    # get country agregates
    countries_df = src2.groupby(['country_src']).agg({
        'domestic': 'sum',
        'international': 'sum'
    })

    # save results
    countries_df.to_csv(args.output_file, header=None, index=True)

    msg = f'Process completed!'
    logging.info(msg)
    print(msg)


if __name__ == '__main__':
    main()
