import os, requests, random, math
from datetime import datetime, timezone, timedelta

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WAT = timezone(timedelta(hours=1)) # Nigeria time

def get_fixtures():
    # Free ESPN feed - no key needed
    urls = [
        "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard",
        "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard",
        "https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/scoreboard",
        "https://site.api.espn.com/apis/site/v2/sports/soccer/ger.1/scoreboard",
    ]
    games = []
    for u in urls:
        try:
            r = requests.get(u, timeout=10).json()
            for ev in r.get("events", []):
                comp = ev["competitions"][0]
                home = comp["competitors"][0]
                away = comp["competitors"][1]
                # only upcoming
                if ev["status"]["type"]["state"] == "pre":
                    # simulate realistic SportyBet odds for heavy favorites
                    # in real use, replace with actual SportyBet API scrape
                    odd = round(random.uniform(1.25, 1.48), 2)
                    games.append({
                        "league": r["leagues"][0]["abbreviation"],
                        "time": datetime.fromisoformat(ev["date"].replace("Z","+00:00")).astimezone(WAT),
                        "home": home["team"]["displayName"],
                        "away": away["team"]["displayName"],
                        "pick": f"{home['team']['displayName']} Win",
                        "odd": odd
                    })
        except: pass
    return sorted(games, key=lambda x: x["time"])[:20]

def build_accumulator(games, target=10.0):
    picks, total = [], 1.0
    for g in games:
        if total * g["odd"] <= target*1.2:
            picks.append(g)
            total *= g["odd"]
        if len(picks) >= 6: break
        if total >= target*0.9: break
    return picks, round(total,2)

def format_msg(picks, total):
    now = datetime.now(WAT).strftime("%a %d %b, %H:%M")
    lines = [f"🎯 SportyBet 10-Odd Builder — {now} WAT\n"]
    for i,g in enumerate(picks,1):
        t = g["time"].strftime("%H:%M")
        lines.append(f"{i}. {t} | {g['league']}\n{g['home']} vs {g['away']}\nPick: {g['pick']} @ {g['odd']}\n")
    lines.append(f"🔢 Total Odds: {total:.2f}")
    lines.append("Stake responsibly. Verify odds on SportyBet before placing.")
    lines.append("\n#SportyBet #10Odds")
    return "\n".join(lines)

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode":"HTML"}, timeout=10)

if __name__ == "__main__":
    games = get_fixtures()
    if not games:
        send("⚠️ No upcoming matches found right now. Check back at next run.")
    else:
        picks, total = build_accumulator(games)
        send(format_msg(picks, total))
