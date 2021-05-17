#!/usr/bin/env python3
import csv
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
import unittest

from modules import airports, country_flights


class TestFlightPerCountry(unittest.TestCase):

    src_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(src_dir, "test_data")

    airports_file = os.path.join(data_dir, "airports_test01.dat")
    flights_file = os.path.join(data_dir, "routes_test01.dat")

    def test_country_flight_files(self):

        # process_airport_file
        airport1 = airports.Airport()
        with open(self.airports_file, "r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                airport1.process_airport_row(row)

        # process_flight_file
        flight_per_country = country_flights.FlightPerCountry(
            airport1.airports_by_iata
        )
        with open(self.flights_file, "r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            for row in reader:
                flight_per_country.process_flight(row)

        expected = {
            "Afghanistan": [14, 29],
            "Congo (Brazzaville)": [10, 34],
            "Denmark": [23, 286],
            "Guinea-Bissau": [0, 7],
            "Sweden": [167, 307],
            flight_per_country.unknown_country: [93, 636],
        }

        result = {}
        for country in expected:
            result[country] = flight_per_country.countries[country]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
