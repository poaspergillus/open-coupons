import json
from datetime import datetime

def parse_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y")

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

try:
    with open("coupons.json", "r") as f:
        coupons = json.load(f)

    active_coupons = []
    for c in coupons:
        exp_date = parse_date(c["expiry"])
        if exp_date >= today:
            active_coupons.append(c)

    with open("coupons.json", "w") as f:
        json.dump(active_coupons, f, indent=2)

    print(f"Cleaner ran successfully. {len(active_coupons)} valid coupons remaining.")

except Exception as e:
    print(f"Error running cleaner: {e}")
