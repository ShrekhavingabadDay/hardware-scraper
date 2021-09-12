'''
config file template:

hardvertipus*bot_name*search_term*min_price*max_price

'''

from scrapers import hardverapro
import dotenv

env = dotenv.getenv()

ha_videokartya = env.get("HARDVERAPRO_VIDEOKARTYA")
ha_alaplap = env.get("HARDVERAPRO_ALAPLAP")
ha_tap = env.get("HARDVERAPRO_TAP")

uid_dir = env.get("UID_DIR")
link_dir = env.get("LINK_DIR")
modosito_url = env.get("HARDVERAPRO_MODOSIT")

config_template_map = {
        "videokartya":ha_videokartya,
        "alaplap":ha_alaplap,
        "tap":ha_tap
}

def configure(filepath):

    scrapers = []

    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line[0] != "#" and len(line)>1:
            params = line.split("*")

            scrapers.append(
                hardverapro.hardverapro_scraper(
                    config_template_map[params[0]],
                    modosito_url,
                    uid_dir,
                    link_dir,
                    {
                        "name":params[1],
                        "stext":params[2],
                        "min_price":params[3],
                        "max_price":params[4]
                    }
                )
            )
    return scrapers


