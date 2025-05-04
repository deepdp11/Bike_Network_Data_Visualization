import csv

network_file = "bike_networks_updated.csv"
country_file = "data.csv"
output_file = "final_bike_networks.csv"

# Load country short form → full name 
country_map = {}
with open(country_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        short = row.get("Code", "").strip().upper()
        full = row.get("Name", "").strip()
        if short:
            country_map[short] = full

# Read bike networks and add full country name
updated_rows = []
with open(network_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames + ["Country Name"] if "Country Name" not in reader.fieldnames else reader.fieldnames
    for row in reader:
        short_code = row.get("Country", "").strip().upper()
        country_name = country_map.get(short_code, "Unknown")
        row["Country Name"] = country_name
        updated_rows.append(row)

# Write updated CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Country names added. Output saved to '{output_file}'.")
