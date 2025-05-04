import csv
import requests
import time

BASE_URL = "http://api.citybik.es/v2/networks"
INPUT_CSV = "bike_networks.csv"
OUTPUT_CSV = "bike_networks_updated.csv"

# Function to get the number of stations for a given network ID
def get_station_count(network_id):
    url = f"{BASE_URL}/{network_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()       # Raise HTTPError for bad responses
        data = response.json()           
        stations = data.get("network", {}).get("stations", [])
        if isinstance(stations, list):
            return len(stations)
        else:
            print(f"Unexpected station format for {network_id}")
    except requests.RequestException as e:  # Handle network errors
        print(f"Failed to fetch stations for '{network_id}': {e}")
    return "N/A"

def main():

    updated_rows = []
    # Read the input CSV file
    with open(INPUT_CSV, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Station Count"]    # Add new column for station count

        for row in reader: 
            network_id = row.get("Network_id", "").strip()
            if not network_id:
                print(f"Missing Network_id in row: {row}")
                row["Station Count"] = "N/A"
            else:
                print(f"Fetching station count for '{network_id}'.")
                station_count = get_station_count(network_id)
                row["Station Count"] = station_count
            updated_rows.append(row)
            time.sleep(12.5)  # Prevents overwhelming the API as per the rate limit

    # Write the updated data to a new CSV file
    print("Writing updated data to new CSV.")
    with open(OUTPUT_CSV, mode="w", newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"Station counts added to '{OUTPUT_CSV}'.")

if __name__ == "__main__":
    main()
