import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

base_url = "https://pugetsndtransit.org"
#Alternative: Getting All Transit stops GIS Data from https://www5.kingcounty.gov/sdc?Layer=TRANSITSTOP_POINT

all_route_types = {
    "kingmetro" : [
         "RapidRide",
         "Seattle",
         "Trolley",
         "Express",
         "Streetcar",
         "Ferry"
    ],
    "sounder": [
        "Light Rail",
        "Express",
        "Sound Transit Express"
    ]
}

time_delay = 0.25

#Returns a list of dicts representing each route, with keys {route_name, route_link, route_type}
def parse_route_network_page(page_url, route_types):
    time.sleep(time_delay)
    print("Parsing Network page: ", page_url)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    all_route_headers = [header for header in soup.find_all(class_="routetype")]
    relevant_route_headers = []
    for route_header in all_route_headers:
        for header_string in route_header.strings:
            if header_string.strip() in route_types:
                relevant_route_headers.append( (header_string.strip(),route_header) )

    routes = []
    for route_header_name, route_header_tag in relevant_route_headers:
        route_list = route_header_tag.next_sibling
        for route in route_list:
            route_link = route.find(class_="routelink").a
            routes.append({"route_type": route_header_name, "route_name" : route_link.string.strip(), "route_link" : route_link["href"]})
    return routes


#Returns a list of station URLs (names can be fetched from station pages)
def parse_route_page(page_url):
    time.sleep(time_delay)
    print("Parsing Route page: ", page_url)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")


    stops_tab = soup.find(id="inboundtab")
    if stops_tab == None:
        stops_tab = soup.find(id="outboundtab")
    stops_list = stops_tab.contents

    return [stop.a["href"] for stop in stops_list]



#Returns the station info for a given station, pulled from the page headers in its info block. Also contains stop name in Name field.
def parse_station_page(page_url):
    time.sleep(time_delay)
    print("Parsing Station page: ", page_url)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")

    stop_name = soup.find(class_="page-title").string.strip()
    station_info = soup.find(class_="station_info").find(class_="rght")

    field_names = station_info.find_all("strong")
    station_info_map = {field.string.strip().replace(":","") : field.next_sibling.string.strip() for field in field_names}
    station_info_map["Name"] = stop_name
    return station_info_map


def parse_all_networks():
    routes = []
    for network, network_route_types in all_route_types.items():
        network_url = base_url + "/" + network + "/route"
        routes += parse_route_network_page(network_url, network_route_types)

    print([route["route_name"] for route in routes])

    stations = []
    for route in routes:
        station_urls = parse_route_page(base_url + route["route_link"])
        for station_url in station_urls:
            station_data = parse_station_page(base_url + station_url)
            station_data["Route"] = route["route_name"]
            station_data["Route Type"] = route["route_type"]
            stations.append(station_data)

    station_df = pd.DataFrame(stations)
    
    return station_df

def clean_up_dataframe(station_df):

    station_df["Lat"] = station_df["Coordinates"].str.split(",").str[0].str.strip()
    station_df["Lon"] = station_df["Coordinates"].str.split(",").str[1].str.strip()
    station_df.drop_duplicates(subset=["Name", "Route"], inplace=True)
    station_df.drop(columns=["OneBusAway Stop ID", "Parking Spots", "Coordinates"], inplace=True)


station_df = parse_all_networks()
clean_up_dataframe(station_df)
print(station_df)
station_df.to_csv("stops.csv")