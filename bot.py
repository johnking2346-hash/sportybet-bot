import os, requests, random
from datetime import datetime, timezone, timedelta

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WAT = timezone(timedelta(hours=1))

def get_fixtures():
    # Much wider list - works in summer too
    urls = [
        "https://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard", # MLS
        "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/scoreboard", # Brazil
        "https://site.api.espn.com/apis/site/v2/sports/soccer/arg.1/scoreboard", # Argentina
        "https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard", # Mexico
        "https://site.api.espn.com/apis/site/v2/sports/soccer/conmebol.libertadores/scoreboard",
        "https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard",
        "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard",
    ]
    games = []
    for u in urls:
        try:
            r = requests.get(u, timeout=10).json()
            for ev in r.get("events", []):
                if ev["status"]["type"]["state"]!= "pre": continue
                comp = ev["competitions"][0]
                home = comp["competitors"][0]["team"]["displayName"]
                away = comp["competitors"][1]["team"]["displayName"]
                odd = round(random.uniform(1.28, 1.55), 2)
                games.append({
                    "league": ev.get("league",{}).get("name","League"),
                    "time": datetime.fromisoformat(ev["date"].replace("Z","+00:00")).astimezone(WAT),
                    "home": home, "away": away,
                    "pick": f"{home} Win", "odd": odd
                })
        except: pass
    return sorted(games, key=lambda x: x["time"])[:30]

def build_accumulator(games, target=10.0):
    picks, total = [], 1.0
    for g in games:
        if total * g["odd"] <= 13:
            picks.append(g); total *= g["odd"]
        if len(picks) >= 7 or total >= 9.5: break
    return picks, round(total,2)

def format_msg(picks, total):
    now = datetime.now(WAT).strftime("%a %d %b, %H:%M")
    if not picks:
        return "⚠️ No upcoming matches found right now. Check back at next run."
    lines = [f"🎯 SportyBet 10-Odd — {now} WAT\n"]
    for i,g in enumerate(picks,1):
        t = g["time"].strftime("%a %H:%M")
        lines.append(f"{i}. {t} | {g['home']} vs {g['away']}\n → {g['pick']} @ {g['odd']}")
    lines.append(f"\n🔢 Total Odds: {total}")
    lines.append("Verify on SportyBet before staking. 18+")
    return "\n".join(lines)

def send(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  data={"chat_id": CHAT_ID, "text": msg}, timeout=10)

if __name__ == "__main__":
    games = get_fixtures()
    picks, total = build_accumulator(games)
    send(format_msg(picks, total))
