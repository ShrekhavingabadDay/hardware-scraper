# TODO: * add command configuration possibility

from scrapers import hardverapro
import dotenv
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="$")

env = dotenv.getenv()

waiting_time = 60

db_reset_iteration_counter = 0

db_reset_iteration = 10

uid_dir = env.get("UID_DIR")
link_dir = env.get("LINK_DIR")
modosito_url = env.get("HARDVERAPRO_MODOSIT")

ha_scraper_horde = [

    hardverapro.hardverapro_scraper(
                    env.get("HARDVERAPRO_VIDEOKARTYA"),
                    modosito_url,
                    uid_dir,
                    link_dir,
                    {
                        "name":"5700-as",
                        "stext":"5700",
                        "min_price":"",
                        "max_price":""
                    }
                ),
    hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"H81 PRO",
                "stext":"h81+pro",
                "min_price":"",
                "max_price":""
            }
        ),
 hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"H110 PRO",
                "stext":"h110+pro",
                "min_price":"",
                "max_price":""
            }
        ),
 hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"H110 D3A",
                "stext":"h110+d3a",
                "min_price":"",
                "max_price":""
            }
        ),
    hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"H81",
                "stext":"h81",
                "min_price":"",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_ALAPLAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"B250",
                "stext":"b250",
                "min_price":"",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_VIDEOKARTYA"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"5700XT",
                "stext":"5700xt",
                "min_price":"",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_VIDEOKARTYA"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"580",
                "stext":"580",
                "min_price":"90000",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_VIDEOKARTYA"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"570",
                "stext":"570",
                "min_price":"90000",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_VIDEOKARTYA"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"3080",
                "stext":"3080",
                "min_price":"600000",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_VIDEOKARTYA"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"3070",
                "stext":"3070",
                "min_price":"420000",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_TAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"Táp - 1200 W",
                "stext":"1200 W",
                "min_price":"",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_TAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"Táp - 1200 Watt",
                "stext":"1200 Watt",
                "min_price":"",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_TAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"Táp - 1200W",
                "stext":"1200W",
                "min_price":"",
                "max_price":""
            }
        ),
hardverapro.hardverapro_scraper(
            env.get("HARDVERAPRO_TAP"),
            modosito_url,
            uid_dir,
            link_dir,
            {
                "name":"Táp - 1200Watt",
                "stext":"1200Watt",
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

@bot.command()
async def beallit(ctx, name, param, value):
    for ha_scraper in ha_scraper_horde:
        if ha_scraper.get_param("name") == name:
            ha_scraper.set_param(param, value)
            await ctx.send("{} {} paramétere beállítva {} értékre".format(name, param, value))
            return

@bot.command()
async def botlista(ctx):
    botlista = ""
    for ha_scraper in ha_scraper_horde:
        botlista += "Név: {} - keresés: {}\n".format(ha_scraper.get_param("name"), ha_scraper.get_param("stext"))

    await ctx.send(botlista)

@bot.event
async def on_ready():
    print("A bot aktív")

bot.loop.create_task(_background_task())
bot.run(env.get("DISCORD_TOKEN"))


