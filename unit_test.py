from scrapers import hardverapro
import dotenv
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

env = dotenv.getenv()

waiting_time = 60

ha_scraper = hardverapro.hardverapro_scraper(
                env.get("HARDVERAPRO"),
                env.get("HARDVERAPRO_MODOSIT"),
                env.get("UID_DIR"),
                env.get("LINK_DIR"),
                "processzor"
            )

ha_scraper.init_session("uj")

ha_scraper.scrape_all_links()

def create_link_message():
    all_links = ha_scraper.scrape_all_links()
    return '\n.\n.'.join(all_links)

async def _background_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(id=817122060618825771)
    while not bot.is_closed():
        message_to_send = create_link_message()

        if message_to_send != '':
            await channel.send('Új hirdetések\n' + message_to_send)
        else:
            await channel.send('Nincs új hirdetés')

        await asyncio.sleep(waiting_time)

@bot.event
async def on_ready():
    print("A bot aktív")

bot.loop.create_task(_background_task())
bot.run(env.get("DISCORD_TOKEN"))


