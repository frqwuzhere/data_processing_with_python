import requests
import pandas as pd
import os

API_URL = "https://server.cekat.ai/messages/sent-from-api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6Ikx4UmFtRVFJRTRseTJKaTgiLCJ0eXAiOiJKV1QifQ.eyJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc2ODM3OTIwNn1dLCJhcHBfbWV0YWRhdGEiOnsiYml6X2lkIjoiMGU2OGY0NGMtMDBhZC00OTg3LWExNjQtYTVlM2JkYTFiMTRjIiwicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwiYXVkIjoiYXV0aGVudGljYXRlZCIsImVtYWlsIjoicHVuZ2t5LnNlcHRpYXdhbkB0ZW1hbmJhaWsuaWQiLCJleHAiOjE3Njg5ODM5NDAsImlhdCI6MTc2ODM3OTIwNiwiaXNfYW5vbnltb3VzIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly91ZHF4dWNsbndsaXNlaXlxdWFyYy5zdXBhYmFzZS5jby9hdXRoL3YxIiwicGhvbmUiOiIiLCJyb2xlIjoiYXV0aGVudGljYXRlZCIsInNlc3Npb25faWQiOiJmYzJhYmVmYy03ODQ0LTQ3YjItYjUxZS0yYzZkZjk3OTJkNmEiLCJzdWIiOiI4NDM4OTU1NS1lMGQwLTQxMDktOTBhZS04YjEwZDM4MWQwYzYiLCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiUHVuZ2t5IENTIn19.MsTz5SZJ_VpK-awwNpG8qypZwcRbMkna7uw5hTjdCJY"

LIMIT = 100
page = 1

all_rows = []

os.makedirs("downloads", exist_ok=True)

while True:
    print(f"Requesting page {page}...")

    try:
        r = requests.get(
            API_URL,
            headers={"Access_token": ACCESS_TOKEN},
            params={"page": page, "limit": LIMIT},
            timeout=30
        )

        if r.status_code != 200:
            print(f"Skipping page {page} — HTTP {r.status_code}")
            page += 1
            continue

        json_data = r.json()
        data = json_data.get("data", [])

        # stop only when last page is reached
        if not data:
            print("Reached last page. Stopping.")
            break

        rows = [{
            "phone_number": item.get("conversation", {})
            .get("contact", {})
            .get("phone_number"),
            "status": item.get("status"),
            "error": item.get("error")
        } for item in data]

        all_rows.extend(rows)

    except Exception as e:
        print(f"Error on page {page}, skipping. Reason: {e}")

    page += 1

pd.DataFrame(all_rows).to_excel(
    "downloads/messages_all_pages.xlsx", index=False
)

print("\nDone. All pages saved.")
