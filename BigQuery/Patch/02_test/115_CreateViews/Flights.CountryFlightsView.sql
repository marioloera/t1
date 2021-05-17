CREATE OR REPLACE VIEW Flights.CountryFlightsView AS

WITH

  CteUnkownCountry AS (
    SELECT 'unknown' AS UnkownCountry
    ),

  CteFlights AS (
    /*
    Get SourceCountry, DestinationCountry Per flight
    */
    SELECT
      COALESCE(Source.Country, CteUnkownCountry.UnkownCountry) AS SourceCountry,
      COALESCE(Destination.Country, CteUnkownCountry.UnkownCountry) AS DestinationCountry

    FROM Flights.Routes, CteUnkownCountry

      LEFT JOIN Flights.Airports AS Source
        ON Routes.SourceAirport = Source.IATA

      LEFT JOIN Flights.Airports AS Destination
        ON Routes.DestinationAirport = Destination.IATA
    ),

  CteCountryFlights AS (
    /*
      determine if a flight is domestic or internationl
      flights with unknown DestinationCountry, will be added to unknown SourceCountry
    */
    SELECT
      CASE WHEN DestinationCountry = CteUnkownCountry.UnkownCountry
        THEN CteUnkownCountry.UnkownCountry
        ELSE SourceCountry
        END AS Country,
      SUM(CASE WHEN SourceCountry = DestinationCountry  THEN 1 ELSE 0 END) AS DomesticFlights,
      SUM(CASE WHEN SourceCountry != DestinationCountry THEN 1 ELSE 0 END) AS InternationalFlights
    FROM CteFlights, CteUnkownCountry
    GROUP BY 1
    )

SELECT *
FROM CteCountryFlights
ORDER BY Country;
