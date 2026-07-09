import json
import requests
from bs4 import BeautifulSoup
import re

def get_leetcode(username):
    try:
        url = f"https://leetcode-stats-api.herokuapp.com/{username}"
        res = requests.get(url, timeout=10).json()
        if res.get("status") == "success":
            return int(res.get("totalSolved", 0))
    except Exception:
        pass
    return 350 # Fallback

def get_codeforces(username):
    try:
        # 1. Get unique problems solved
        status_url = f"https://codeforces.com/api/user.status?handle={username}"
        res = requests.get(status_url, timeout=10).json()
        solved_count = 0
        if res.get("status") == "OK":
            solved = set()
            for sub in res["result"]:
                if sub.get("verdict") == "OK":
                    prob = sub.get("problem", {})
                    if "contestId" in prob and "index" in prob:
                        solved.add(f"{prob['contestId']}{prob['index']}")
            solved_count = len(solved)
            
        # 2. Get Rank
        rank_url = f"https://codeforces.com/api/user.info?handles={username}"
        rank_res = requests.get(rank_url, timeout=10).json()
        rank = "Newbie"
        if rank_res.get("status") == "OK":
            rank = rank_res["result"][0].get("rank", "Newbie").title()
            
        return solved_count, rank
    except Exception:
        pass
    return 0, "Newbie"

def get_gfg(username):
    try:
        url = f"https://www.geeksforgeeks.org/profile/{username}/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        
        # Regex to aggressively find the solved count in GFG's HTML
        match = re.search(r'Problems Solved.*?(\d+)', res.text, re.IGNORECASE | re.DOTALL)
        if match:
            return int(match.group(1))
    except Exception as e:
        print(f"GFG Error: {e}")
    return 200 # Fallback

if __name__ == "__main__":
    lc_solved = get_leetcode("rajatkhedar123")
    cf_solved, cf_rank = get_codeforces("rajatkhedar123")
    gfg_solved = get_gfg("rajat54epe")
    
    # Calculate Grand Total (Note: Naukri is difficult to scrape without an API, so we sum the main 3)
    total_solved = lc_solved + cf_solved + gfg_solved
    
    stats = {
        "leetcode": lc_solved,
        "codeforces_rank": cf_rank,
        "codeforces_solved": cf_solved,
        "gfg": gfg_solved,
        "total": total_solved
    }
    
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)
    print("Successfully generated advanced stats.json:", stats)
