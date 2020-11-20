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
    # 14104: Russia
    print(f"14104: {aiports.get('14104', '?')}")

    countries = init_countries(aiports)
    print(f"Uruguay: {countries['Uruguay']}")

    # proces flights 

def get_airports(file_path):
    airportIdIndex = 0
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

def get_flights(file_path):
    try:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)

            for row in reader:
                pass
    except OSError as ex:
        print(ex)
        pass


if __name__ == '__main__':
    main()
    print('clean exit')
