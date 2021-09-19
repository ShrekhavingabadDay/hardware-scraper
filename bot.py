# TODO: * add command configuration possibility

from scrapers import hardverapro
import dotenv
import asyncio
from discord.ext import commands
import scraper_config

bot = commands.Bot(command_prefix="$")

env = dotenv.getenv()

waiting_time = 60

db_reset_iteration_counter = 0

db_reset_iteration = 10

ha_scraper_horde = scraper_config.configure(env.get("CONFIG_FILE_PATH"))

for ha_scraper in ha_scraper_horde: 
    ha_scraper.init_session("uj")
    ha_scraper.scrape_all_links()

def reset_dbs():
    ha_scraper.reset_db()

def create_link_message():
    
    final_message_object = {}    

    for ha_scraper in ha_scraper_horde:
        bot_result = ha_scraper.scrape_all_links()

        if bot_result:
            final_message_object[bot_result["hardvertipus"]] = bot_result["message"]

    return final_message_object

async def _background_task():
    await bot.wait_until_ready()

    db_reset_iteration_counter = 0

    while not bot.is_closed():

        db_reset_iteration_counter += 1


        if db_reset_iteration_counter == db_reset_iteration:

            db_reset_iteration_counter = 0
            
            reset_dbs()

            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.name == "általános":
                        await channel.send("ver0.9.2 - Ping")

            continue
        
        message_object_to_send = create_link_message()

        for key in message_object_to_send:
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.name == key:
                        try:
                            await channel.send(message_object_to_send[key])
                        # handle case of too many new ads = too long message
                        except:
                            message_to_send = message_object_to_send[key]
                            i = 0
                            while i < (len(message_to_send) - 1):

                                message_end_index = max(200, len(message_to_send) - i - 1)

                                await channel.send(message_to_send[i:(i+message_end_index)])

                                i+=message_end_index


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


