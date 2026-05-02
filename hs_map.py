import folium
from folium.plugins import LocateControl, MeasureControl
import pandas as pd
import random


quarter_mile_meters = 402.336
ONLY_INCLUDE_SEATTLE = False

default_off = ["Seattle", "Trolley", "Sound Transit Express"]
custom_icons = {
    "Light Rail" : "train",
    "Ferry": "ferry"
}

route_type_colors = {
    "Light Rail" : "blue",
    "Ferry": "darkblue",
    "Streetcar": "red"
}



#Inspired by https://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/
def generate_programmatic_random_color(name):
    random.seed(name)
    color_code = f"#{random.randrange(255):2x}{random.randrange(255):2x}{random.randrange(255):2x}"
    return color_code

def populate_map():
    base_map = folium.Map(location = (47.6061, -122.3328))
    stops = pd.read_csv("stops.csv")

    route_types = stops["Route Type"].unique()
    route_layers = {route_type: folium.FeatureGroup(route_type, show = False if route_type in default_off else True).add_to(base_map) for route_type in route_types}


    for i, stop in stops.iterrows():
        if ONLY_INCLUDE_SEATTLE and stop["City"] != "Seattle":
            continue
        stop_color = generate_programmatic_random_color(stop["Route"])

        folium.Marker(
            location = (stop["Lat"], stop["Lon"]),
            popup = stop["Name"],
            icon = folium.Icon(
                color= route_type_colors[stop["Route Type"]] if stop["Route Type"] in route_type_colors else "orange",
                icon=  custom_icons[stop["Route Type"]] if stop["Route Type"] in custom_icons else "bus",
                prefix = "fa")
        ).add_to(route_layers[stop["Route Type"]])

        folium.Circle(
            location = (stop["Lat"], stop["Lon"]),
            radius = quarter_mile_meters,
            stroke = True,
            color = stop_color,
            fill_color = stop_color,
            fill = False,
            opacity = 1,
            fillOpacity = 0.2
        ).add_to(route_layers[stop["Route Type"]])
    folium.LayerControl(hideSingleBase=True).add_to(base_map)
    LocateControl().add_to(base_map)
    MeasureControl(primary_length_unit="miles", secondary_length_unit="meters").add_to(base_map)
    base_map.save("seattle.html" if ONLY_INCLUDE_SEATTLE else "seattle_metro.html")

populate_map()