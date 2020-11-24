#!/usr/bin/env python3

import unittest

from modules import country_flights


class TestFlightPerCountry(unittest.TestCase):

    IataCountry = {
        "ARN": "Sweden",
        "GOT": "Sweden",
        "LAX": "United States",
        "ELP": "United States",
    }

    AirpotIdCountry = {
        737: "Sweden",
        687: "Sweden",
        3484: "United States",
        3559: "United States",
        -2: "Mexico"
    }

    FlightDataA = [
        (00, 000, "ARN", 737, "GOT", 687, 0, 0, 135),
        (00, 000, "ARN", 737, "ELP", 3559, 0, 0, 135),
        (00, 410, "LAX", 2965, "GOT", 687, 0, 0, 135),
        (00, 410, "LAX", 2966, "ELP", 3559, 0, 0, 135),
        (00, 410, "LAX", 2966, "XXX", -1, 0, 0, 135),
        (00, 410, "ZZZ", -2, "ELP", 3559, 0, 0, 135),
        (00, 410, "XXX", -1, "YYY", -2, 0, 0, 135),
    ]

    def test_get_airport_country_by_iata(self):
        flightPerCountry = country_flights.FlightPerCountry(self.IataCountry)
        expected = self.IataCountry
        result = {}
        for iata in self.IataCountry:
            result[iata] = flightPerCountry.get_airport_country(
                airport_code=iata
            )
        self.assertEqual(result, expected)

    def test_get_airport_country_mix(self):
        flightPerCountry = country_flights.FlightPerCountry(
            airports_by_iata=self.IataCountry,
            airports_by_id=self.AirpotIdCountry)
        expected = self.IataCountry
        result = {}
        for iata in self.IataCountry:
            result[iata] = flightPerCountry.get_airport_country(
                airport_code=iata)
        self.assertEqual(result, expected)

    def test_get_unknown_country(self):
        flightPerCountry = country_flights.FlightPerCountry({})
        expected = flightPerCountry.unknown_country
        result = flightPerCountry.get_airport_country("KIO")
        self.assertEqual(result, expected)

    def test_get_country_flights(self):
        """this can check partial results, order not important
        for example United States is exluded in the test
        but is pressent in the flightPerCountry.countries
        """
        flightPerCountry = country_flights.FlightPerCountry(self.IataCountry)

        expected = {
            flightPerCountry.unknown_country: [1, 2],
            # "United States": [1, 1],
            "Sweden": [1, 1],
        }

        for row in self.FlightDataA:
            flightPerCountry.process_flight(row)

        result = {}
        for country in expected:
            result[country] = flightPerCountry.countries[country]

        self.assertEqual(result, expected)

    def test_get_country_flights_2(self):
        """  this can check partial results, order not important
            for example United States is exluded in the test 
            but is pressent in the flightPerCountry.countries
            include airport without iata code and airportid(-2) Mexico
        """
        flightPerCountry = country_flights.FlightPerCountry(
            airports_by_iata=self.IataCountry,
            airports_by_id=self.AirpotIdCountry)

        expected = {
            flightPerCountry.unknown_country: [0, 2],
            "United States": [1, 1],
            "Sweden": [1, 1],
            "Mexico": [0, 1]
        }

        for row in self.FlightDataA:
            flightPerCountry.process_flight(row)

        result = {}
        for country in expected:
            result[country] = flightPerCountry.countries[country]

        self.assertEqual(result, expected)

    def test_result_format(self):
        """this can check full results, order important
        results are list of list.
        """

        flightPerCountry = country_flights.FlightPerCountry(self.IataCountry)

        expected = [
            ["Sweden", 1, 1],
            ["United States", 1, 1],
            [flightPerCountry.unknown_country, 1, 2],
        ]

        for row in self.FlightDataA:
            flightPerCountry.process_flight(row)

        result = flightPerCountry.get_results_format1()

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
