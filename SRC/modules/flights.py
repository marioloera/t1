#!/usr/bin/env python3


class FlightsColumns:

    airline = 0
    airline_id = 1
    source_airport = 2
    source_airport_id = 3
    destination_airport = 4
    destination_airport_id = 5
    codeshare = 6
    stops = 7
    equipment = 8

    __list__ = [
        name
        for name in tuple(locals())
        if not (name.startswith("__") and name.endswith("__"))
    ]
