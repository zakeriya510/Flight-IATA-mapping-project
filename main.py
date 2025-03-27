import pandas as pd
import folium
from IPython.display import display

# URLs for the datasets
airport_database = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
route_database = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat'

# Column names for airport dataset
airport_columns = ['Airport_ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz_database', 'Type', 'Source']
route_columns = ['Airline', 'Airline_ID', 'Source_Airport', 'Source_Airport_ID', 'Destination_Airport', 'Destination_Airport_ID', 'Codeshare', 'Stops', 'Equipment']

# Load datasets
airport_refined = pd.read_csv(airport_database, names=airport_columns, dtype=str)
route_refined = pd.read_csv(route_database, names=route_columns, dtype=str)

# Function to fetch coordinates of an airport by IATA code
def find_coordinates(airport_iata):
    airport_credential = airport_refined[airport_refined["IATA"] == airport_iata]
    if not airport_credential.empty:
        latitude_coordinates = float(airport_credential.iloc[0]["Latitude"])
        longitude_coordinates = float(airport_credential.iloc[0]["Longitude"])
        return latitude_coordinates, longitude_coordinates
    else:
        return None

# Function to fetch airline and equipment details
def get_equipment(source_iata, dest_iata):
    route_credential = route_refined[(route_refined["Source_Airport"] == source_iata) & (route_refined["Destination_Airport"] == dest_iata)]
    if not route_credential.empty:
        equipment_detail = route_credential.iloc[0]["Equipment"]
        airline_name = route_credential.iloc[0]["Airline"]
        return f"Carrier: {airline_name}, Equipment: {equipment_detail}"
    else:
        return "Flight details unavailable"

# Function to plot the flight route
def plotting_route(source_iata, dest_iata):
    source_coordinates = find_coordinates(source_iata)
    destination_coordinates = find_coordinates(dest_iata)

    if source_coordinates is None or destination_coordinates is None:
        print("No geospatial details fetched for inputted IATA-coded airfields.")
        return

    flight_info = get_equipment(source_iata, dest_iata)

    # Finding midpoint for better visualization
    mid1 = (source_coordinates[0] + destination_coordinates[0]) / 2
    mid2 = (source_coordinates[1] + destination_coordinates[1]) / 2
    midpoint = (mid1, mid2)

    # Creating a map centered at the midpoint
    flight_map = folium.Map(location=midpoint, zoom_start=3)

    # Adding markers for source and destination airports
    folium.Marker(source_coordinates,
                  popup=f"Source: {source_iata}",
                  icon=folium.Icon(color='blue')).add_to(flight_map)

    folium.Marker(destination_coordinates,
                  popup=f"Destination: {dest_iata}\n{flight_info}",  # Displaying airline & equipment
                  icon=folium.Icon(color='red')).add_to(flight_map)

    # Drawing a line between source and destination
    folium.PolyLine([source_coordinates, destination_coordinates],
                    color="blue", weight=2.5, opacity=1).add_to(flight_map)

    # Display the map
    display(flight_map)

# User inputs source and destination IATA codes
source_iata = input("Enter Source Airport IATA Code: ").upper()
destination_iata = input("Enter Destination Airport IATA Code: ").upper()

# Call the function with user inputs
plotting_route(source_iata, destination_iata)

