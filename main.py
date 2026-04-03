import asyncio
import aiohttp
import json
import random
import threading
from datetime import datetime


AUTH_TOKEN  = ""
SUPER_PROPS = ""


# This is in milliseconds
GATHER_TIME = 50 /1000
MIN_REST    = 30 /1000  
REST_RANGE  = 0  /1000

def get_timestamp():
    return f"[{datetime.now().strftime('%H:%M:%S')}]"

class GorillaBot:
    def __init__(self, token):
        self.token = token
        self.user_id = "430772757643395074"
        self.current_xp = 0
        self.is_running = True
        
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "X-Super-Properties": SUPER_PROPS,
            "Accept": "*/*",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me/1480221451838816428",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

    async def start_loop(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            print("-" * 40)
            print(f"User ID: {self.user_id}")
            print(f"Super Props: {SUPER_PROPS[:10]}**********")
            print("-" * 40)

            while self.is_running:
                try:
                    async with session.post("https://discord.com/api/v9/gorilla/activity/gathering/start", json={}) as resp:
                        if resp.status not in [200, 204]:
                            err = await resp.text()
                            print(f"{get_timestamp()} [START]  -> {resp.status}: {err}")
                        else:
                            print(f"{get_timestamp()} [START]  -> XP: {self.current_xp}")

                    await asyncio.sleep(GATHER_TIME)

                    payload = {
                        "user_data": {
                            "user_id": self.user_id,
                            "crafting_class": "armor_crafter",
                            "combat_class": "dps",
                            "has_started_gathering": False,
                            "xp": self.current_xp + 100
                        }
                    }

                    async with session.post("https://discord.com/api/v9/gorilla/activity/gathering/complete", json=payload) as resp:
                        if resp.status == 200:
                            try:
                                data = await resp.json()
                                self.current_xp = data["user_data"]["xp"]
                                print(f"{get_timestamp()} [COMPLETE] log  -> New XP: {self.current_xp}")
                            except Exception:
                                self.current_xp += 100
                                print(f"{get_timestamp()} [COMPLETE] log  -> XP: {self.current_xp}")
                        else:
                            err = await resp.text()
                            print(f"{get_timestamp()} [COMPLETE] Error  -> {resp.status}: {err}")

                    await asyncio.sleep(MIN_REST + (random.random() * REST_RANGE))

                except Exception as e:
                    print(f"{get_timestamp()} Loop Exception: {e}")
                    await asyncio.sleep(5)

def bot_thread_worker():
    bot = GorillaBot(token=AUTH_TOKEN)
    asyncio.run(bot.start_loop())

if __name__ == "__main__":
    t = threading.Thread(target=bot_thread_worker, daemon=True)
    t.start()
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("Stopping...")