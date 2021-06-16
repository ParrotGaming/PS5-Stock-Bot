from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
from bs4 import BeautifulSoup, re
import asyncio
import random

from scraping_lib.target import *
from scraping_lib.gamestop import *
from scraping_lib.bestbuy import *
from scraping_lib.micromania import *
from scraping_lib.amazon import *

target_url = "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596"
gamestop_url = "https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html"
bestbuy_url = "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"
micromania_url = "https://www.micromania.fr/playstation-5-alldigital-106097.html"
amazon_url = "https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG"

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

prefix = "!PS"

bot = commands.Bot(command_prefix = prefix)

opts = Options()
opts.add_argument('--no-sandbox')
opts.add_argument('--lang=en_US') 
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_argument('--headless')
opts.add_argument('--user-agent=User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"')
opts.add_argument('--disable-dev-shm-usage')

chrome_driver = os.getcwd() +"/linux_chromedriver"

driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

driver.set_window_size(1920,1080)

async def update_status(id, in_stock):
    # US
    if os.getenv("ENVIRONMENT") == 'dev':
        channel = bot.get_channel(712801808590045296)
    elif os.getenv("ENVIRONMENT") == 'prod':
        channel = bot.get_channel(846860248865177630)
    footer_text = "https://www.buymeacoffee.com/PS5StockBot"
    if id == 1:
        if in_stock == False:
            embed=discord.Embed(title="Target", url=target_url, description="There are currently no PS5s in stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="Target", url=target_url, description="PS5s are in stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
    elif id == 2:
        if in_stock == False:
            embed=discord.Embed(title="Best Buy", url=bestbuy_url, description="There are currently no PS5s in stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="Best Buy", url=bestbuy_url, description="PS5s are in stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
    elif id == 3:
        if in_stock == False:
            embed=discord.Embed(title="GameStop", url=gamestop_url, description="There are currently no PS5s in stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="GameStop", url=gamestop_url, description="PS5s are in stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
    elif id == 5:
        if in_stock == False:
            embed=discord.Embed(title="Amazon", url=amazon_url, description="There are currently no PS5s in stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="Amazon", url=amazon_url, description="PS5s are in stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
    #FR
    elif id == 4:
        if os.getenv("ENVIRONMENT") == 'dev':
            channel = bot.get_channel(847927342462795838)
        elif os.getenv("ENVIRONMENT") == 'prod':
            channel = bot.get_channel(847929825884766239)
        footer_text="https://www.buymeacoffee.com/PS5StockBot"
        if in_stock == False:
            embed=discord.Embed(title="MircoMania", url=micromania_url, description="Il n'y a actuellement aucune PS5 en stock.", color=0xFF5733)
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)
        if in_stock == True:
            embed=discord.Embed(title="MicroMania", url=micromania_url, description="Les PS5 sont en stock!", color=discord.Color.green())
            embed.set_footer(text=footer_text)
            await channel.send(embed=embed)

async def send_screenshot():
    driver.save_screenshot("screenshot.png")
    if os.getenv("ENVIRONMENT") == 'dev':
        await bot.get_channel(712801808590045296).send(file=discord.File('screenshot.png'))
    if os.getenv("ENVIRONMENT") == 'prod':
        await bot.get_channel(846860248865177630).send(file=discord.File('screenshot.png'))

@tasks.loop(seconds=30)
async def scrape():
    await scrape_target(driver, send_screenshot, update_status, target_url)
    await scrape_gamestop(driver, send_screenshot, update_status, gamestop_url)
    await scrape_best_buy(driver, send_screenshot, update_status, bestbuy_url)
    await scrape_micromania(driver, send_screenshot, update_status, micromania_url)
    await scrape_amazon(driver, send_screenshot, update_status, amazon_url)
    if os.getenv("ENVIRONMENT") == 'prod':
        await bot.get_channel(846905034422878258).send("All Trackers Online")

@bot.event
async def on_ready():
    print('[on_ready] start scrape')
    scrape.start()

@bot.command()
async def start(ctx):
    print('[start] start scrape')
    scrape.start()

bot.run(token)