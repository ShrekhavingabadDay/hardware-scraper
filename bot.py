# TODO: * add command configuration possibility

from scrapers import hardverapro
import dotenv
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

env = dotenv.getenv()

waiting_time = 60

db_reset_iteration_counter = 0

db_reset_iteration = 10

ha_scraper_horde = [

    hardverapro.hardverapro_scraper(
                    env.get("HARDVERAPRO_VIDEOKARTYA"),
                    env.get("HARDVERAPRO_MODOSIT"),
                    env.get("UID_DIR"),
                    env.get("LINK_DIR"),
                    {
                        "name":"5700-as",
                        "stext":"5700",
                        "min_price":"",
                        "max_price":""
                    }
                ),
    hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            env.get("HARDVERAPRO_MODOSIT"),
            env.get("UID_DIR"),
            env.get("LINK_DIR"),
            {
                "name":"H81 PRO",
                "stext":"h81+pro",
                "min_price":"",
                "max_price":""
            }
        ),
 hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            env.get("HARDVERAPRO_MODOSIT"),
            env.get("UID_DIR"),
            env.get("LINK_DIR"),
            {
                "name":"H110 PRO",
                "stext":"h110+pro",
                "min_price":"",
                "max_price":""
            }
        ),
 hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            env.get("HARDVERAPRO_MODOSIT"),
            env.get("UID_DIR"),
            env.get("LINK_DIR"),
            {
                "name":"H110 D3A",
                "stext":"h110+d3a",
                "min_price":"",
                "max_price":""
            }
        ),



]

for ha_scraper in ha_scraper_horde: 
    ha_scraper.init_session("uj")
    ha_scraper.scrape_all_links()

def reset_dbs():
    ha_scraper.reset_db()

def create_link_message():
    all_messages = ""
    for ha_scraper in ha_scraper_horde:
        try:
            all_messages += "\n." + ha_scraper.scrape_all_links()
        except TypeError:
            pass
    return all_messages

async def _background_task():
    await bot.wait_until_ready()

    db_reset_iteration_counter = 0

    while not bot.is_closed():

        db_reset_iteration_counter += 1


        if db_reset_iteration_counter == db_reset_iteration:

            db_reset_iteration_counter = 0

            reset_dbs()
            continue
        
        message_to_send = create_link_message()

        if message_to_send:
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    await channel.send(message_to_send)

        await asyncio.sleep(waiting_time)

@bot.event
async def on_ready():
    print("A bot aktív")

bot.loop.create_task(_background_task())
bot.run(env.get("DISCORD_TOKEN"))


