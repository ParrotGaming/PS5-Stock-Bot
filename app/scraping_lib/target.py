import asyncio
from bs4 import BeautifulSoup, re

target_status = False
target_confirms = 0

async def scrape_target(driver, send_screenshot, update_status, url):
    global target_status
    global target_confirms

    print("starting target scrape\n\n")

    driver.delete_all_cookies()

    driver.get(url)

    await asyncio.sleep(5)

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("div", {"data-test": "soldOutBlock"})
    
    if not sold_out:
        print("(Target) IN STOCK!!!!!\n\n")
        target_confirms += 1
        if target_status == False:
            if target_confirms >= 2:
                await send_screenshot()
                await update_status(1, True)
                target_status = True
    else:
        print("(Target) sold out :(\n\n")
        target_confirms = 0
        if target_status == True:
            await send_screenshot()
            await update_status(1, False)
            target_status = False