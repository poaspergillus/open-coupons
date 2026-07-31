import json
import csv
import urllib.request
from datetime import datetime

# REPLACE THIS with your actual Google Sheet ID
SHEET_ID = "16yD_VGjraHtVVzk7QuOJH44D8R4ydJYC_vpXXtflPsk" 

csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

try:
    response = urllib.request.urlopen(csv_url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    reader = csv.reader(lines)
    next(reader) # Skip the header row
    
    active_coupons = []
    for row in reader:
        if len(row) < 5: continue 
        
        # Row layout: [Timestamp, Store, Description, Code, Expiry]
        try:
            exp_date = datetime.strptime(row[4].strip(), "%d/%m/%Y")
            if exp_date >= today:
                active_coupons.append({
                    "title": row[1].strip(),
                    "description": row[2].strip(),
                    "code": row[3].strip(),
                    "expiry": row[4].strip()
                })
        except ValueError:
            continue # Skip rows with bad date formats

    with open("coupons.json", "w") as f:
        json.dump(active_coupons, f, indent=2)

    print(f"Updated from Sheet. {len(active_coupons)} valid coupons.")

except Exception as e:
    print(f"Error: {e}")
