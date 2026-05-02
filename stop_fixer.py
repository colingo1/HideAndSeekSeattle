import pandas as pd



address_map = {
    #Light Rail stations, which have exact address rather than a City like everything else:
    "Redmond Technology Station" : "Redmond, WA",
    "Overlake Village Station" : "Redmond, WA",
    "BelRed Station" : "Bellevue, WA",
    "Spring District Station" : "Bellevue, WA",
    "Wilburton Station" : "Bellevue, WA",
    "Bellevue Downtown" : "Bellevue, WA",
    "East Main Bellevue Station" : "Bellevue, WA",
    "Tukwila International Blvd Station" : "Tukwila, WA",
    "Rainier Beach Station" : "Seattle, WA",
    "Othello Station" : "Seattle, WA",
    "Columbia City Station" : "Seattle, WA",
    "Mt. Baker Station" : "Seattle, WA",
    "Beacon Hill Station" : "Seattle, WA",
    "SODO Station" : "Seattle, WA",
    "Stadium Station": "Seattle, WA",
    "Capitol Hill Link Station" : "Seattle, WA",
    "University of Washington / Husky Stadium Station" : "Seattle, WA",
    "U District Station" : "Seattle, WA",
    "Roosevelt Station" : "Seattle, WA",
    "Northgate Station" : "Seattle, WA",
    "Shoreline South/148th Station" : "Shoreline, WA",
    "Shoreline North/185th Station" : "Shoreline, WA",
    "Mountlake Terrace Station" : "Mountlake Terrace, WA",
    "Lynnwood City Center Station" : "Lynnwood, WA",
    "Old City Hall Station" : "Tacoma, WA",

    #Some other assorted stations that happen to be missing an Address field:
    "Alaskan Way S & S Jackson St" : "Seattle, WA",
    "NE 75th St & 25th Ave NE" : "Seattle, WA",
    "S Jackson St & 12th Ave S" : "Seattle, WA",
    "Kelly Rd NE & 320th Way NE" : "Lake Marcel-Stillwater, WA",
    "Tolt Ave & W Rutherford St" : "Carnation, WA",
    "SR 203 & W Bird St" : "Carnation, WA",
    "SR 203 & NE 40th St" : "Carnation, WA",
    "SE 42nd Pl & 334th Pl SE" : "Fall City, WA",
    "SE Redmond Fall City Rd & 337th Pl SE" : "Fall City, WA",
    "SE Fall City-Snoqualmie Rd & 356th Ave SE" : "Fall City, WA",
    "SE Fall City-Snoqualmie Rd & 361st Ave SE" : "Fall City, WA",
    "SE Fall City-Snoqualmie Rd & 367th Ave SE" : "Fall City, WA",
    "Delridge Way SW & SW Findlay St" : "Seattle, WA",
    "Delridge Way SW & SW Holden St" : "Seattle, WA",
    "SW Roxbury St & 26th Ave SW" : "Seattle, WA",
    "15th Ave SW & SW Roxbury St - Bay 1" : "White Center, WA",
    "15th Ave SW & SW 102nd St" : "White Center, WA",
    "15th Ave SW & SW 106th St" : "White Center, WA",
    "Vashon Passenger Ferry & Vashon Ferry Dock" : "Vashon, WA",
    "Bellevue Transit Center - Bay 6" : "Bellevue, WA"

}




#Fixes a few stops, which for some reason have some errors in their actual site data.
def fix_addresses(stops):
    for (stop_name, real_address) in address_map.items():
        stops.loc[stops["Name"] == stop_name, ["Address"]] = real_address

#Removes a few unnecessary fields, and makes other fields better to read.
def clean_up_dataframe(stops):

    stops["Lat"] = stops["Coordinates"].str.split(",").str[0].str.strip()
    stops["Lon"] = stops["Coordinates"].str.split(",").str[1].str.strip()
    stops["City"] = stops["Address"].str.split(",").str[0].str.strip()
    stops.drop_duplicates(subset=["Name", "Route"], inplace=True)
    stops.drop(columns=["OneBusAway Stop ID", "Parking Spots", "Coordinates", "Agency Stop ID", "Address"], inplace=True)


stops = pd.read_csv("stops_raw.csv")
fix_addresses(stops)
clean_up_dataframe(stops)

stops.to_csv("stops.csv", index=False)
