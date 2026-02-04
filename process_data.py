
import json
import csv
import glob
import os
import re

def parse_number_string(s):
    if not s or s == "N/A":
        return 0
    s = s.strip().upper()
    multiplier = 1
    if s.endswith('K'):
        multiplier = 1000
        s = s[:-1]
    elif s.endswith('M'):
        multiplier = 1000000
        s = s[:-1]
    
    try:
        if '<' in s:
            s = s.replace('<', '')
        return float(s) * multiplier
    except ValueError:
        return 0

def clean_value(v):
    if v is None:
        return "N/A"
    return str(v)

all_data = []

# Load all batch files
batch_files = glob.glob('batch*.json')
batch_files.sort()

for f in batch_files:
    with open(f, 'r') as json_file:
        data = json.load(json_file)
        all_data.extend(data)

# Sort by Sold count (descending) as a default useful view
# We need to parse the "Sold" field which is a string like "1.5K"
all_data.sort(key=lambda x: parse_number_string(x.get('Sold', '0')), reverse=True)

# Write to CSV
keys = ["UserID", "UserName", "Seller Rating", "Reviews", "Average Ship", "Sold", "Following", "Followers"]
csv_file_path = 'seller_data.csv'

with open(csv_file_path, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    for row in all_data:
        # Ensure all keys exist
        row_clean = {k: clean_value(row.get(k, "N/A")) for k in keys}
        dict_writer.writerow(row_clean)

# Write combined JSON
with open('seller_data.json', 'w') as json_out:
    json.dump(all_data, json_out, indent=2)

print(f"Combined {len(all_data)} profiles.")
print(f"Saved to {csv_file_path} and seller_data.json")

# Generate a quick summary
top_5_sold = all_data[:5]
print("\nTop 5 Sellers by Items Sold:")
for s in top_5_sold:
    print(f"- {s['UserName']} ({s['UserID']}): {s['Sold']} sold")
