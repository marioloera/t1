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

    # airport & flights columns class
    airports_col = airports.AirportColumns()
    flights_col = flights.FlightsColumns()
    # print(airports_col.__list__) # object

    # create dataframes from csv input files
    # airports_df = pd.read_csv(airports_file)
    # airports_df = pd.read_csv(airports_file, header=None)
    airports_df_all = pd.read_csv(airports_file, names=airports_col.__list__)
    flights_df_all = pd.read_csv(flights_file, names=flights_col.__list__)

    # remove columns not needed so the join contains less columns
    flights_df = flights_df_all.iloc[9:15, [
        flights_col.source_airport,
        flights_col.destination_airport,
    ]]

    airports_df = airports_df_all.iloc[:, [
        airports_col.iata,
        airports_col.country,
    ]]

    # normal extraction
    # for i, flight_row in flights_df.iterrows():
    #     source_airport = flight_row[flights_col.source_airport]
    #     destination_airport = flight_row[flights_col.destination_airport]
    #     print(i, source_airport, source_airport_id, destination_airport,
    #           destination_airport_id)

    # pands merge by col names source airpot ai
    src1 = flights_df.merge(airports_df,
                            left_on='source_airport',
                            right_on='iata')

    # print('\nsrc1\n')
    # print(src1)
    # print(src1.columns)
    # # x2 = flights_df.merge(airports_df, left_on=flights_df.columns[flights_col.source_airport], right_on=airports_df.columns[airports_col.iata])
    # # print(x2)

    # print(src1[['source_airport', 'destination_airport', 'country']])

    src2 = src1.merge(airports_df,
                      left_on='destination_airport',
                      right_on='iata',
                      suffixes=('_src', '_dest'))

    print('\nsrc2\n')
    #print(src2)
    #print(src2.columns)
    print(src2[['country_src', 'country_dest']])

    # add domestic or international

    #src2['test'] = src2.apply(lambda row: row.country_src + row.country_dest, axis=1)
    # fn = lambda row: row.country_src + row.country_dest
    # fn = lambda row: row.country_src == row.country_dest
    # src2['test2'] = src2.apply(fn, axis=1)

    fn_domestic = lambda row: 1 if row.country_src == row.country_dest else 0
    fn_international = lambda row: 1 if row.country_src != row.country_dest else 0
    src2['domestic'] = src2.apply(fn_domestic, axis=1)
    src2['international'] = src2.apply(fn_international, axis=1)

    # df1.iloc[1:5, 2:4]
    print(src2.iloc[:, 2:])

    # get country agregates
    countries_df = src2.groupby(['country_src']).agg({
        'domestic': 'sum',
        'international': 'sum'
    })
    print(countries_df)

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
