import discord
from discord.ext import commands, tasks
import asyncio
import pandas as pd
from stockcheker2 import Scraper
import numpy as np
import time



def main():

    link1 = 'https://www.tokopedia.com/nvidiageforce/etalase/geforce-gtx-16-series'

    description = ''' 
    Bot buat ngecek alert stock GPU sekitaran MSRP
    Bot made using discord API wrapper for python: https://github.com/Rapptz/discord.py
    Scraping uses Selenium and BeautifulSoup4 in python
    Bot Made By zokovi (discord:zokovi#1021)
              '''

    help_command = commands.DefaultHelpCommand(no_category = 'Commands List')

    intents = discord.Intents.default()
    #intents.members = True
    bot = commands.Bot(command_prefix='!', description=description, intents=intents, help_command=help_command)
    #bot.add_cog(a(bot))


    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        active_calculating = discord.Game(name='Updating GPU Stock... Bot may be unresponsive, just wait')
        active_ready = discord.Game(name='Ready, type !help for help commands')
        while True:
                try:
                        await bot.change_presence(status=discord.Status.dnd, activity=active_calculating)
                        scraper1 = Scraper()
                        scraper1.scrape_page(link1)
                        scraper1.df.to_csv('data.csv')
                        await bot.change_presence(status=discord.Status.online, activity=active_ready)
                        await asyncio.sleep(15)
                except Exception as e:
                        print(e)
                        await asyncio.sleep(15)

    @bot.command(description='Pong')
    async def ping(ctx):
        await ctx.send('pong')
    

    @bot.command(description='Show links where the bot is checking stock from.')
    async def listlinks(ctx):
        
        link_list = [link1
        ]
        link_list_str = [f'\n > {x}' for x in link_list]
        link_list_str = ' '.join(link_list_str)

        msg = f'Checking stock from: {link_list_str}'

        await ctx.send(msg)
    
           

    @bot.command(description='Notifikasi (mention) kalo ada stock, to stop just send "stop" to channel. \n "!StockNotification  1" to also receive notification when no stock available.')
    async def StockNotification(ctx, no_stock_notification= 0):
        if ctx.author.id == bot.user.id:
            return

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        stopped = False

        try:
            df = pd.read_csv('data.csv', index_col=0)
            df_stock = df[df['Stock'].str.contains('Stok Habis') == False]
            time_now = time.time()
            
            if df_stock.empty == False:
                msg = f'{ctx.author.mention} Ada Stock'
                await ctx.send(msg)
                for index, item in df_stock.iterrows():
                    await ctx.send(item.values)
                stopped = True

            else:
                if no_stock_notification == 1:
                    msg = f'No stock yet'
                    await ctx.send(msg)
                stopped = False

        except Exception as e:
            print(e)

                    
        while not stopped:
            try:
                message = await bot.wait_for("message", check=check, timeout=5)
                stopped = True if message.content.lower() == "stop" else False
                
            except asyncio.TimeoutError: # make sure you've imported asyncio
                try:
                    df = pd.read_csv('data.csv', index_col=0)
                    df_stock = df[df['Stock'].str.contains('Stok Habis') == False]
                    time_now = time.time()
                    
                    if df_stock.empty == False:
                        msg = f'{ctx.author.mention} Ada Stock'
                        await ctx.send(msg)
                        for index, item in df_stock.iterrows():
                            await ctx.send(item.values)
                        stopped = True
                    else:
                        if no_stock_notification == 1:
                            msg = f'No stock yet'
                            await ctx.send(msg)
                        stopped = False

                except Exception as e:
                    print(e)
                    await ctx.send('Bot have an error')
                    stopped = True
                    
        await ctx.send("Notification Stopped")

    bot.run('TOKEN')
    #


if __name__ == '__main__':
    main()





