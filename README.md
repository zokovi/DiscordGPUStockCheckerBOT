# DiscordGPUStockCheckerBOT

Bot buat ngecek alert stock GPU sekitaran MSRP

Bot made using discord API wrapper for python: https://github.com/Rapptz/discord.py

Scraping uses Selenium and BeautifulSoup4 in python.

This bot currently scrapes from Nvidia Geforce Official Store in Tokopedia.


## Requirements
1. Selenium and driver (ex. geckodriver)

    > pip install Selenium

    > https://github.com/mozilla/geckodriver/releases

2. BeautifulSoup4

    > pip3 install beautifulsoup4

3. lxml-parser

    > pip3 install lxml

4. discord.py 

    > pip3 install discord.py
    

## Usage
1. Install Requirements (advised to use virtualenv) and put the driver to ./bin/

2. Change TOKEN in the main.py to your discord bot tokens.

3. Run the main.py (activate virutalenv first if you're using virtualenv)

    > python3 main.py


## Future Updates

  Change bot to use cog
