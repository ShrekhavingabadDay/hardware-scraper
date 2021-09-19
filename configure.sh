# create directories
mkdir data && cd data && mkdir ids && mkdir links &&

# create config file with template
touch .default_scraperconfig &&

echo "# hardvertipus*bot_neve*keresesi_ertek*min_ar*max_ar" >> .default_scraperconfig &&

touch .env_template &&

echo "HARDVERAPRO_MODOSIT=\"https://hardverapro.hu/muvelet/beallitasok/modosit.php?mode=uad&url=\"" >> .env_template &&

printf "HARDVERAPRO_VIDEOKARTYA=\"https://hardverapro.hu/aprok/hardver/videokartya/keres.php?stext=&county=&stcid=&settlement=&stmid=&minprice=&maxprice=&company=&user=&usrid=&selling=1&buying=1&stext_none=&search_exac=1\"\nHARDVERAPRO_ALAPLAP=\"https://hardverapro.hu/aprok/hardver/alaplap/keres.php?stext=&county=&stcid=&settlement=&stmid=&minprice=&maxprice=&company=&user=&usrid=&selling=1&buying=1&stext_none=&search_exac=1\"\nHARDVERAPRO_TAP=\"https://hardverapro.hu/aprok/hardver/haz_tapegyseg/keres.php?stext=&county=&stcid=&settlement=&stmid=&minprice=&maxprice=&company=&user=&usrid=&selling=1&buying=1&stext_none=&search_exac=1\"\n" >> .env_template &&

echo "UID_DIR=\"$(pwd)/data/ids\"" >> .env_template &&

echo "LINK_DIR=\"$(pwd)/data/links\"" >> .env_template &&

echo "CONFIG_FILE_PATH=\"$(pwd)/.scraperconfig\"" >> .env_template &&

echo "DISCORD_TOKEN=\"\"" >> .env_template

