import json
import requests
from bs4 import BeautifulSoup

def get_leetcode(username):
    try:
        url = f"https://leetcode-stats-api.herokuapp.com/{username}"
        res = requests.get(url, timeout=10).json()
        if res.get("status") == "success":
            return f"{res.get('totalSolved')}"
    except Exception:
        pass
    return "350+"

def get_codeforces(username):
    try:
        url = f"https://codeforces.com/api/user.info?handles={username}"
        res = requests.get(url, timeout=10).json()
        if res.get("status") == "OK":
            rank = res["result"][0].get("rank", "Pupil")
            return rank.title()
    except Exception:
        pass
    return "Pupil"

def get_gfg(username):
    try:
        url = f"https://www.geeksforgeeks.org/profile/{username}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        stat_element = soup.find(string=lambda text: text and ("Problems Solved" in text or "Total Problems Solved" in text))
        if stat_element:
            parent = stat_element.find_parent()
            value = parent.find_next_sibling() or parent
            return value.text.strip()
    except Exception:
        pass
    return "200+"

if __name__ == "__main__":
    stats = {
        "leetcode": get_leetcode("rajatkhedar123"),
        "codeforces": get_codeforces("rajatkhedar123"),
        "gfg": get_gfg("rajat54epe")
    }
    
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)
    print("Successfully updated stats.json with:", stats)
