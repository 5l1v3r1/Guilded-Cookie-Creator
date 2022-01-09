import asyncio
import aiohttp
import os
import logging

os.system('clear')

logging.basicConfig(
    level=logging.INFO, 
    format="\u001b[38;5;215m[\u001b[38;5;255m%(asctime)s\u001b[38;5;215m] \u001b[38;5;255m-> \u001b[38;5;215m%(message)s", 
    datefmt=f"%I:%M:%S"
)

brown = "\u001b[38;5;215m"
reset = "\u001b[38;5;255m"

class Scraper:

    def __init__(self, debug: bool):
        self.debug = debug
        self.proxy_type = input("%s[%s?%s] %sProxytype %s[%ssocks4/socks5/http%s]:%s " % (brown, reset, brown, reset, brown, reset, brown, reset))

    async def scrape(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=%s&timeout=10000&country=all&ssl=all&anonymity=all" % (self.proxy_type)) as r:
                f = open("proxies.txt", "wb")
                f.write(await r.read())
                f.close()
                logging.info("Proxy Succesfully Scraped")
                input()
                exit()

if __name__ == "__main__":
    client = Scraper(
        debug=False
    )
    try:
        asyncio.run(client.scrape())
    except Exception as e:
        print(e)
        input()
        exit()
