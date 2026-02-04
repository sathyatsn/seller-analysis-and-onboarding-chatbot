
import json
import csv

def parse_sold(val):
    if not val or val == "N/A":
        return 0
    val = str(val).upper().strip()
    multiplier = 1
    if val.endswith('K'):
        multiplier = 1000
        val = val[:-1]
    elif val.endswith('M'):
        multiplier = 1000000
        val = val[:-1]
    
    try:
        if '<' in val:
            val = val.replace('<', '')
        return float(val) * multiplier
    except ValueError:
        return 0

def clean_data(input_file, output_json, output_csv):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Filter rules: 
    # 1. Rating must not be null/None
    # 2. Sold count must be present (not N/A)
    cleaned_data = []
    
    for entry in data:
        rating = entry.get('Seller Rating')
        sold = entry.get('Sold')
        
        # Check if invalid
        if rating is None or rating == "N/A":
            continue
        if sold is None or sold == "N/A":
            continue
            
        # Cleaned entry
        cleaned_data.append(entry)

    print(f"Original Clean Count: {len(data)}")
    print(f"Cleaned Count: {len(cleaned_data)}")

    # Save JSON
    with open(output_json, 'w') as f:
        json.dump(cleaned_data, f, indent=2)

    # Save CSV
    if cleaned_data:
        keys = cleaned_data[0].keys()
        with open(output_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(cleaned_data)
    
    print(f"Saved to {output_json} and {output_csv}")

if __name__ == "__main__":
    clean_data('seller_data.json', 'clean_seller_data.json', 'clean_seller_data.csv')
