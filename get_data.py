import requests
import pandas as pd
import os

API_URL = "https://server.cekat.ai/messages/sent-from-api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6Ikx4UmFtRVFJRTRseTJKaTgiLCJ0eXAiOiJKV1QifQ.eyJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc2NTQyMjU3NH1dLCJhcHBfbWV0YWRhdGEiOnsiYml6X2lkIjoiMGU2OGY0NGMtMDBhZC00OTg3LWExNjQtYTVlM2JkYTFiMTRjIiwicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwiYXVkIjoiYXV0aGVudGljYXRlZCIsImVtYWlsIjoicHVuZ2t5LnNlcHRpYXdhbkB0ZW1hbmJhaWsuaWQiLCJleHAiOjE3NjYwMjczMDgsImlhdCI6MTc2NTQyMjU3NCwiaXNfYW5vbnltb3VzIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly91ZHF4dWNsbndsaXNlaXlxdWFyYy5zdXBhYmFzZS5jby9hdXRoL3YxIiwicGhvbmUiOiIiLCJyb2xlIjoiYXV0aGVudGljYXRlZCIsInNlc3Npb25faWQiOiJiNjUwOWM1My1iOTI3LTRkNDQtYTk3ZC00YzRmNGUwZTM3NzYiLCJzdWIiOiI4NDM4OTU1NS1lMGQwLTQxMDktOTBhZS04YjEwZDM4MWQwYzYiLCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiUHVuZ2t5IENTIn19.TizvC3tDYMBCxfLDDgHscEq446Uq711tlT2RqEau_Hw"

LIMIT = 100
page = 1

all_rows = []

os.makedirs("downloads", exist_ok=True)

while True:
    print(f"Requesting page {page}...")

    r = requests.get(
        API_URL,
        headers={"Access_token": ACCESS_TOKEN},
        params={"page": page, "limit": LIMIT}
    )

    if r.status_code != 200:
        print("API error:", r.status_code, r.text)
        break

    data = r.json().get("data", [])

    # auto-stop on last page
    if not data:
        print("Reached last page. Stopping.")
        break

    # parse
    rows = [{
        "phone_number": item.get("conversation", {}).get("contact", {}).get("phone_number"),
        "status": item.get("status"),
        "error": item.get("error")
    } for item in data]

    all_rows.extend(rows)

    # pd.DataFrame(rows).to_excel(
    #     f"downloads/messages_page_{page}.xlsx", index=False)
    # print(f"Saved page {page}")

    page += 1

pd.DataFrame(all_rows).to_excel(
    "downloads/messages_all_pages.xlsx", index=False)
print("\nDone. All pages saved.")
