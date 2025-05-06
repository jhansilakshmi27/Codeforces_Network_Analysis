import requests
import networkx as nx
import pandas as pd
from tqdm import tqdm
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
})

#Fetching top 100 rated users
def get_top_100_users():
    url = "https://codeforces.com/api/user.ratedList?activeOnly=true"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        users = [user["handle"] for user in data["result"][:1000]]
        return users
    except Exception as e:
        print("Error fetching top users:", e)
        return []

#all problems with metadata (tags, rating)
def get_all_problems():
    url = "https://codeforces.com/api/problemset.problems"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        problems = data["result"]["problems"]
        problem_map = {}

        for problem in problems:
            contest_id = problem.get("contestId")
            index = problem.get("index")
            if contest_id and index:
                problem_id = (contest_id, index)
                name = f"{contest_id}-{index}"
                tags = ",".join(problem.get("tags", []))
                rating = problem.get("rating", "")
                title = problem.get("name", "")
                problem_map[problem_id] = {
                    "id": name,
                    "label": name,
                    "title": title,
                    "tags": tags,
                    "rating": rating,
                    "type": "Problem"
                }

        return problem_map
    except Exception as e:
        print("Error fetching problems:", e)
        return {}

# Step 3: Get solved problems for a user
def get_user_solved_problems(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        submissions = response.json().get("result", [])

        solved = set()
        for sub in submissions:
            if sub.get("verdict") == "OK":
                prob = sub.get("problem", {})
                problem_id = (prob.get("contestId"), prob.get("index"))
                if all(problem_id):
                    solved.add(problem_id)

        return solved
    except Exception as e:
        print(f"Error fetching submissions for {handle}:", e)
        return set()

def build_graph_and_export(user_handles, problem_map):
    nodes = []
    edges = []

    for prob in problem_map.values():
        nodes.append({
            "Id": prob["id"],
            "Label": prob["label"],
            "Type": prob["type"],
            "Tags": prob["tags"],
            "Rating": prob["rating"],
            "Title": prob["title"]
        })

    for user in tqdm(user_handles, desc="Processing users"):
        nodes.append({"Id": user, "Label": user, "Type": "User", "Tags": "", "Rating": "", "Title": ""})
        solved = get_user_solved_problems(user)
        for prob in solved:
            if prob in problem_map:
                edges.append({"Source": user, "Target": problem_map[prob]["id"]})
        time.sleep(0.6)

    nodes_df = pd.DataFrame(nodes)
    edges_df = pd.DataFrame(edges)

    nodes_df.to_csv("nodes.csv", index=False)
    edges_df.to_csv("edges.csv", index=False)
    print("Exported nodes.csv and edges.csv with tags/ratings for Gephi.")

if __name__ == "__main__":
    user_handles = get_top_100_users()
    print(f"Fetched top {len(user_handles)} users.")

    problem_map = get_all_problems()
    print(f"Fetched {len(problem_map)} problems with metadata.")

    build_graph_and_export(user_handles, problem_map)

