# Kaparó [HardverApróhoz](https://hardverapro.hu)

Discord bot, ami megadott konfigurációk alapján értesítést küld a birtokában lévő discord szerverekre, hardvertípusonként csatornákra osztva az újdonságokat.

## Telepítés, konfigurálás és futtatás:

## Szükséges szoftverek:
- python3
- pip3:
  - virtualenv

## Konfigurálás:
1. `sh configure.sh`: ez előállítja a *.env_tamplate* és *.default_scraperconfig* fájlokat, amikben a konfigurációhoz szükséges minden további tudnivaló megtalálható.
2. `python3 -m virtualenv venv` létrehozza a python virtuális környezetet
3. `[source ( ez shellfüggő ) ]./venv/bin/activate` aktiválja a virtuális környezetet
4. `pip install -r requirements.txt` telepíti a szoftver futtatásához szükséges python csomagokat

## Futtatás:
`python3 bot.py` vagy `screen python3 bot.py` majd `ctrl+d` és `ctrl+a` hogy elkerüljük a program kimenetének fő shellszessönre való kiiratását
