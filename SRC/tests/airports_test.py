#!/usr/bin/env python3

import unittest

from modules import airports


class TestAirport(unittest.TestCase):

    AirportData1 = [
        (
            3484,
            "Los Angeles International Airport",
            "Los Angeles",
            "United States",
            "LAX",
            "KLAX",
            33.94250107,
            -118.4079971,
            125,
            -8,
            "A",
            "America/Los_Angeles",
            "airport",
            "OurAirports",
        ),
        (
            737,
            "Stockholm-Arlanda Airport",
            "Stockholm",
            "Sweden",
            "ARN",
            "ESSA",
            59.651901245117,
            17.918600082397,
            137,
            1,
            "E",
            "Europe/Stockholm",
            "airport",
            "OurAirports",
        ),
    ]

    def test_airports_by_id(self):
        airport1 = airports.Airport()
        for row in self.AirportData1:
            airport1.process_airport_row(row)
        id1 = 737
        id2 = 3484
        expected = [
            (id1, "Sweden"),
            (id2, "United States"),
        ]
        result = [
            (id1, airport1.airports_by_id[id1]),
            (id2, airport1.airports_by_id[id2]),
        ]
        self.assertEqual(result, expected)

    def test_airports_by_iata(self):
        airport1 = airports.Airport()
        for row in self.AirportData1:
            airport1.process_airport_row(row)
        Iata1 = "ARN"
        Iata2 = "LAX"
        expected = [
            (Iata1, "Sweden"),
            (Iata2, "United States"),
        ]
        result = [
            (Iata1, airport1.airports_by_iata[Iata1]),
            (Iata2, airport1.airports_by_iata[Iata2]),
        ]
        self.assertEqual(result, expected)

    def test_airports_by_icao(self):
        airport1 = airports.Airport()
        for row in self.AirportData1:
            airport1.process_airport_row(row)
        icao1 = "ESSA"
        icao2 = "KLAX"
        expected = [
            (icao1, "Sweden"),
            (icao2, "United States"),
        ]
        result = [
            (icao1, airport1.airports_by_icao[icao1]),
            (icao2, airport1.airports_by_icao[icao2]),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
