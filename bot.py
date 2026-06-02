import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Render will inject these from Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_todays_picks():
    """Demo picks - replace with real Sportybet scraper later"""
    try:
        url = "https://www.sportybet.com/ng/sport/football/today"
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)'}
        r = requests.get(url, headers=headers, timeout=15)
        
        # For now just return demo data - Sportybet blocks simple scrapers
        # We'll add Selenium later for the real booking code
        picks = [
            {"match": "Arsenal vs Chelsea", "market": "Home Win", "odds": 1.85},
            {"match": "Barcelona vs Real Madrid", "market": "Over 2.5", "odds": 1.70},
            {"match": "Man City vs Liverpool", "market": "BTTS Yes", "odds": 1.65},
            {"match": "Bayern vs Dortmund", "market": "Home Win", "odds": 1.95},
        ]
        return picks
    except Exception as e:
        # Fallback demo
        return [
            {"match": "Demo Game 1", "market": "1X", "odds": 1.80},
            {"match": "Demo Game 2", "market": "Over 1.5", "odds": 1.60},
            {"match": "Demo Game 3", "market": "Home Win", "odds": 2.10},
        ]

async def send_daily_picks():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("ERROR: Missing TELEGRAM_TOKEN or CHAT_ID")
        return
        
    bot = Bot(TELEGRAM_TOKEN)
    picks = get_todays_picks()
    
    total_odds = 1
    msg = "📌 *SportyBet 10-Odd Bot - TEST*\n\n"
    
    for i, p in enumerate(picks[:4], 1):
        total_odds *= p["odds"]
        msg += f"{i}. {p['match']}\n   {p['market']} @ {p['odds']}\n\n"
        if total_odds >= 9.5:
            break
    
    msg += f"*Total Odds: {total_odds:.2f}*\n"
    msg += f"*Model Chance: ~12-15%*\n\n"
    msg += "✅ Bot is live on Render!\n"
    msg += "Next: Add real Sportybet scraper + booking code"
    
    await bot.send_message(
        chat_id=CHAT_ID, 
        text=msg, 
        parse_mode='Markdown'
    )
    print("Message sent successfully!")

if __name__ == "__main__":
    asyncio.run(send_daily_picks())
