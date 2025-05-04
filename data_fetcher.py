import requests
import csv

# Base URL for the CityBikes API
base_url = "http://api.citybik.es/v2/networks"

# Fetch JSON data from a URL
def fetch_json(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {url} - {e}")
        return None

# Fetch the list of networks
data = fetch_json(base_url)
if data is None:
    print("No data fetched. Exiting.")
    exit(1)

# Prepare CSV file
csv_filename = "bike_networks.csv"
fields = ["Network_id","Network Name", "City", "Country", "Location_Latitude", "Location_Longitude"]

# Open CSV file for writing
with open(csv_filename, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(fields)

    for network in data["networks"]:
        network_id = network.get("id", "Unknown")
        name = network.get("name", "Unknown")
        location = network.get("location", {})
        city = location.get("city", "Unknown")
        country = location.get("country", "Unknown")
        latitude = location.get("latitude", "Unknown")
        longitude = location.get("longitude", "Unknown")
        

        # Write row to CSV
        writer.writerow([network_id, name, city, country, latitude, longitude])

print(f"Data written to {csv_filename}")
