import Config
import logging
import asyncio
import time
import aiohttp
from pyrogram import Client, idle

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

app = Client(
    ":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="ForceSubscribeBot"),
)

async def sync_time():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://worldtimeapi.org/api/timezone/Etc/UTC") as r:
                data = await r.json()
                current_utc_time = data["unixtime"]
                local_time = int(time.time())
                delta = current_utc_time - local_time
                print(f"[INFO] Selisih waktu: {delta} detik")
                return abs(delta) <= 5
    except Exception as e:
        print(f"[WARNING] Gagal sync waktu: {e}")
        return False

async def start_bot():
    for attempt in range(5):
        if await sync_time():
            try:
                await app.start()
                print("✅ Bot berhasil start.")
                await app.idle()
                return
            except Exception as e:
                print(f"[ERROR] Gagal start Pyrogram: {e}")
        else:
            print(f"[WAIT] Waktu belum sinkron, coba lagi 5 detik... ({attempt+1}/5)")
        await asyncio.sleep(5)

    print("❌ Gagal sinkron waktu setelah 5 percobaan. Stop bot.")
    exit(1)

if __name__ == "__main__":
    asyncio.run(start_bot())
