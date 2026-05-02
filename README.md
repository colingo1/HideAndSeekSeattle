Scripts and display logic for playing Jet Lag Hide and Seek in the Seattle area.

Scripts:

kc_station_scraper.py: pulls Seattle area transit stations across multiple transportation methods,
and gets stop name and location. Writes stop data to stops.csv.

hs_map.py: 
Reads from stops CSV and generates a map of Seattle with 0.25 mile radius areas around each stop.
Written to seattle.html

TODO:
Add better disambiguation of stops, with better colors.
Potentially add some ability to draw on the map, for things like radars and thermometers.
