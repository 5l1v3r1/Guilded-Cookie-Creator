#credit to fweak for the "stag" generator <3
import asyncio
import aiohttp
import os
import secrets
import hashlib
import uuid
import random

from tasksio import TaskPool
from util.Logging import logging

if os.name == "posix":
    os.system("clear")
else:
    os.system("cls")

class Guilded(object):

    def __init__(self):
        self.colors = {
            "red": "\x1b[38;5;203m",
            "reset": "\x1b[0m"
        }

        self.username = input("{}[{}~{}] {}Username {}->{} ".format(self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"]))
        self.invite = input("{}[{}~{}] {}Invite {}->{} ".format(self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"]))
        self.proxy_type = input("{}[{}~{}] {}Proxytype {}->{} ".format(self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"]))
        self.tasks = int(input("{}[{}~{}] {}Tasks {}->{} ".format(self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"], self.colors["red"], self.colors["reset"])))

        print()

        with open("data/proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]
    
    def get_headers(self, email: str):
        client_id = str(uuid.uuid1())
        device_id = secrets.token_hex(64)

        email_format = '{}-{}-'.format(email, email)
        generating_stag = hashlib.md5(email_format.encode())
        stag = generating_stag.hexdigest()

        logging.info("Obtained Client ID {}-> {}{}".format(self.colors["reset"], self.colors["red"], client_id))
        logging.info("Obtained Device ID {}-> {}{}".format(self.colors["reset"], self.colors["red"], device_id))
        logging.info("Obtained Stag {}-> {}{}".format(self.colors["reset"], self.colors["red"], stag))

        return {
            'Content-Type': 'application/json',
            'guilded-client-id': client_id,
            'guilded-device-id': device_id,
            'guilded-device-type': 'desktop', 
            'guilded-stag': stag,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.153'
        }
    
    async def create(self):
        try:
            name = "{} | {}".format(self.username, secrets.token_hex(8))
            email = "bottedaccount+{}@gmail.com".format(secrets.token_urlsafe(5))
            password = secrets.token_hex(10)

            headers = self.get_headers(email)
            proxy_format = "{}://{}".format(self.proxy_type, random.choice(self.proxies))

            json = {
                "extraInfo": {"platform": "desktop"},
                "name": name,
                "email": email,
                "password": password,
                "fullName": name
            }

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post("https://www.guilded.gg/api/users?type=email", json=json, proxy=proxy_format) as client:
                    async with session.post("https://www.guilded.gg/api/login", json={'email': email, 'password': password, 'getMe': True}, proxy=proxy_format) as response:
                        if response.status == 200:
                            cookies = str(response.cookies)
                            session = cookies.split('hmac_signed_session=')[1].split(';')[0]
                            logging.info("Created {}-> {}{}************".format(self.colors["reset"], self.colors["red"], session[:22]))
                            async with open("data/cookies.txt", "w") as r:
                                await r.write("{}\n".format(session))
                            return session
                        else:
                            pass
        except Exception as e:
            pass
    
    async def join(self):
        try:
            headers = {"cookie": "hmac_signed_session={}".format(await self.create())}
            proxy_format = "{}://{}".format(self.proxy_type, random.choice(self.proxies))

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.put("https://www.guilded.gg/api/invites/{}".format(self.invite), proxy=proxy_format) as r:
                    if r.status == 200:
                        logging.info("Succesfully Joined {}-> {}{}".format(self.colors["reset"], self.colors["red"], self.invite))
                    else:
                        pass
        except Exception as e:
            logging.error(e)

    async def start(self):
        async with TaskPool(self.tasks) as pool:
            while True:
                await pool.put(self.join())

if __name__ == "__main__":
    client = Guilded()
    asyncio.run(client.start())
