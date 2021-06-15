import asyncio
from bs4 import BeautifulSoup, re

amazon_status = False
amazon_confirms = 0

async def scrape_amazon(driver, send_screenshot, update_status, url):
    global amazon_status
    global amazon_confirms
    print("starting amazon scrape\n\n")

    driver.delete_all_cookies()

    driver.get(url)

    await asyncio.sleep(5)
    
    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')
    
    sold_out = soup.find_all("span", text="Currently unavailable.")

    if not sold_out:
        print("(Amazon) IN STOCK!!!!!\n\n")
        amazon_confirms += 1
        if amazon_status == False:
            if amazon_confirms >= 2:
                await send_screenshot()
                await update_status(5, True)
                amazon_status = True
    else:
        print("(Amazon) sold out :(\n\n")
        amazon_confirms = 0
        if amazon_status == True:
            await send_screenshot()
            await update_status(5, False)
            amazon_status = False