import asyncio
from bs4 import BeautifulSoup, re

micromania_status = False
micromania_confirms = 0

async def scrape_micromania(driver, send_screenshot, update_status, url):
    global micromania_status
    global micromania_confirms
    print("starting micromania scrape\n\n")

    driver.delete_all_cookies()

    driver.get(url)

    await asyncio.sleep(5)

    soup_file=driver.page_source
    soup = BeautifulSoup(soup_file, 'html.parser')

    sold_out = soup.find_all("span", text="Produit disponible en magasin uniquement.")

    print(sold_out)

    if sold_out:
        print("(MicroMania) IN STOCK!!!!!\n\n")
        micromania_confirms += 1
        if micromania_status == False:
            if micromania_confirms >= 2:
                await send_screenshot()
                await update_status(4, True)
                micromania_status = True
    else:
        print("(MicroMania) sold out :(\n\n")
        micromania_confirms = 0
        if micromania_status == True:
            await send_screenshot()
            await update_status(4, False)
            micromania_status = False