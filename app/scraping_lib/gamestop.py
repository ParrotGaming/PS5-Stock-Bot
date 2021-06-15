import asyncio
from bs4 import BeautifulSoup, re

gamestop_status = False
gamestop_confirms = 0

async def scrape_gamestop(driver, send_screenshot, update_status, url):
    global gamestop_status
    global gamestop_confirms
    print("starting gamestop scrape\n\n")

    driver.delete_all_cookies()

    driver.get("https://www.gamestop.com/")

    await asyncio.sleep(5)

    driver.get(url)

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("button", {"data-pid": "11108140"})

    if not sold_out:
        print("(GameStop) IN STOCK!!!!!\n\n")
        gamestop_confirms += 1
        if gamestop_status == False:
            if gamestop_confirms >= 2:
                await send_screenshot()
                await update_status(3, True)
                gamestop_status = True
    else:
        print("(GameStop) sold out :(\n\n")
        gamestop_confirms = 0
        if gamestop_status == True:
            await send_screenshot()
            await update_status(3, False)
            gamestop_status = False