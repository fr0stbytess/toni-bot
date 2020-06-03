"""This is the core file of our Discord bot
   Claude."""


import discord
import requests as r

from sys import exit
from json import load, dump
from geopy.geocoders import Nominatim

from modules import components

try:
    with open("data/settings.json", "r") as f:
        data = load(f)
except Exception:
    print("Error")


class Application(discord.Client):
    """Core class for core processing"""

    async def on_ready(self):
        print("Initialized client as ", self.user)
        try:
            game = discord.Game(data["status"])
            status = discord.Status.idle
            await claude.change_presence(status=status, activity=game)
        except Exception:
            print("something went wrong.")
            exit()

    async def on_message(self, message):
        if message.content.startswith("!status"):
            await message.channel.send("Wait a moment, let me check.")
            try:
                r.get("https://lcroleplay.com/", verify=False)
                await message.channel.send("Website is working fine.")
            except r.exceptions.ConnectionError as conn_e:
                await message.channel.send("Error: {}".format(conn_e))
            except r.exceptions.HTTPError as http_e:
                await message.channel.send("Error: {}".format(http_e))
            except r.exceptions.Timeout as conn_t:
                await message.channel.send("Error: {}".format(conn_t))

        if message.content.startswith("!weather"):
            locate = "New York City"
            geolocator = Nominatim(
                user_agent=components.user_agent)
            location = geolocator.geocode(locate)
            weather = r.get(components.darksky_line.format(
                location.latitude, location.longitude))
            with open("data/weather.json", "w") as f:
                dump(weather.json(), f, indent=4)
            with open("data/weather.json", "r+") as weather:
                weather_data = load(weather)
            await message.channel.send(
                "LC Weather: {}".format(weather_data["currently"]["summary"]
                                        ))


claude = Application()
claude.run(data["token"])
