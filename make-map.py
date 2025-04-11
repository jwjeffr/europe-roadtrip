import json
from pathlib import Path

import folium
from geopy.geocoders import Nominatim


with Path("coordinates.json").open("r") as file:

    COORDINATES = json.load(file)


def get_coordinates(location):
    try:
        return COORDINATES[location]
    except KeyError:
        geolocator = Nominatim(user_agent="roadtrip_planner")
        if loc := geolocator.geocode(location):
            return loc.latitude, loc.longitude
        raise ValueError("location not found in db nor found by geopy")


# Function to create the map and plot routes
def plot_trip(destinations, routes):
    # Initialize the map centered around the first destination
    start_coords = get_coordinates(destinations[0])
    trip_map = folium.Map(location=start_coords, zoom_start=6)

    # Plot each destination as a marker on the map
    for destination in destinations:
        coords = get_coordinates(destination)
        if coords:
            folium.Marker(coords, popup=destination).add_to(trip_map)

    # Plot routes between destinations
    for i in range(1, len(destinations)):
        start_coords = get_coordinates(destinations[i - 1])
        end_coords = get_coordinates(destinations[i])
        if start_coords and end_coords:
            route_type = routes[i - 1]
            color = "blue"  # Default to blue for driving
            if route_type == "ferry":
                color = "green"
            elif route_type == "flight":
                color = "red"
            elif route_type == "bus":
                color = "orange"

            # Draw the line between the two destinations
            folium.PolyLine([start_coords, end_coords], color=color, weight=3, opacity=0.7).add_to(trip_map)

    # Save the map to an HTML file
    trip_map.save("index.html")
    print("Map saved as 'index.html'.")


def main():

    # Example usage:
    destinations = [
        "Telde, Spain",
        "Laayoune, Morocco",
        "Casablanca, Morocco",
        "Tangier, Morocco",
        "Gibraltar",
        "Porto, Portugal",
        "Madrid, Spain",
        "Barcelona, Spain",
        "Andorra la Vella, Andorra",
        "Marseille, France",
        "Monte Carlo, Monaco",
        "Genoa, Italy",
        "Florence, Italy",
        "Dogana, San Marino",
        "Venice, Italy",
        "Ljubljana, Slovenia",
        "Zagreb, Croatia",
        "Banja Luka, Bosnia and Herzegovina",
        "Sarajevo, Bosnia and Herzegovina",
        "Dubrovnik, Croatia",
        "Tirana, Albania",
        "Athens, Greece",
        "Larnaca, Cyprus",
        "North Nicosia, Northern Cyprus",
        "Beirut, Lebanon",
        "Amman, Jordan",
        "Istanbul, Turkey",
        "Varna, Bulgaria",
        "Bucharest, Romania",
        "Belgrade, Serbia",
        "Budapest, Hungary",
        "Bratislava, Slovakia",
        "Vienna, Austria",
        "Prague, Czechia",
        "Warsaw, Poland",
        "Kaliningrad, Russia",
        "Klaipeda, Lithuania",
        "Riga, Latvia",
        "Tallinn, Estonia",
        "Helsinki, Finland",
        "Turku, Finland",
        "Berghamn, Finland",
        "Grisslehamn, Sweden",
        "Stockholm, Sweden",
        "Gothenburg, Sweden",
        "Copenhagen, Denmark",
        "Lubeck, Germany",
        "Hamburg, Germany",
        "Amsterdam, Netherlands",
        "Antwerp, Belgium",
        "Calais, France",
        "London, United Kingdom",
        "Edinburgh, United Kingdom",
        "Cork, Ireland"
    ]
    routes = [
        "flight",
        "drive",
        "drive",
        "ferry",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "flight",
        "bus",
        "flight",
        "bus",
        "flight",
        "bus",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "bus",
        "bus",
        "drive",
        "drive",
        "ferry",
        "drive",
        "ferry",
        "ferry",
        "drive",
        "drive",
        "drive",
        "ferry",
        "drive",
        "drive",
        "drive",
        "drive",
        "drive",
        "bus",
        "flight"
    ]
    if len(destinations) != len(routes) + 1:
        print(len(routes) + 1, len(destinations))
        raise ValueError
    plot_trip(destinations, routes)


if __name__ == "__main__":

    main()
