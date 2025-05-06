import requests

def get_total_problems():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        problems = data["result"]["problems"]
        print(f"Total number of problems in Codeforces problemset: {len(problems)}")
    else:
        print("Failed to fetch problems.")

get_total_problems()

