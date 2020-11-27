--CREATE OR REPLACE VIEW mll.CountryFlightsView2 AS

WITH

  CteUnkownCountry AS (
    SELECT 'unknown' AS UnkownCountry
    ),

  CteFlights AS (
    /*  
    Get SourceCountry, DestinationCountry Per flight
    */
    SELECT
      COALESCE(S1.Country, S2.Country, CteUnkownCountry.UnkownCountry) AS SourceCountry,
      COALESCE(D1.Country, D2.Country, CteUnkownCountry.UnkownCountry) AS DestinationCountry
    
    FROM mll.Routes, CteUnkownCountry
      -- using IATA
      LEFT JOIN mll.Airports AS S1
        ON Routes.SourceAirport = S1.IATA

      LEFT JOIN mll.Airports AS D1
        ON Routes.DestinationAirport = D1.IATA
     
      -- using AirpotId
      LEFT JOIN mll.Airports AS S2
        ON Routes.SourceAirportId = S2.AirportId

      LEFT JOIN mll.Airports AS D2
        ON Routes.DestinationAirportId = D2.AirportId
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
WHERE Country in ('Canada', 'China', 'Costa Rica', 'United States', 'unknown')
ORDER BY Country