import asyncio
from bs4 import BeautifulSoup, re

bestbuy_status = False
bestbuy_confirms = 0

async def scrape_best_buy(driver, send_screenshot, update_status, url):
    global bestbuy_status
    global bestbuy_confirms
    print("starting best buy scrape\n\n")

    driver.delete_all_cookies()

    driver.get("https://www.bestbuy.com/")

    await asyncio.sleep(5)

    driver.get(url)

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("button", {"class": "add-to-cart-button"})

    if sold_out[0].text != "Sold Out":
        print("(BestBuy) IN STOCK!!!!!\n\n")
        bestbuy_confirms += 1
        if bestbuy_status == False:
            if bestbuy_confirms >= 2:
                await send_screenshot()
                await update_status(2, True)
                bestbuy_status = True
    else:
        print("(BestBuy) sold out :(\n\n")
        bestbuy_confirms = 0
        if bestbuy_status == True:
            await send_screenshot()
            await update_status(2, False)
            bestbuy_status = False