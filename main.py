"""This is the core file of our Discord bot
   Claude."""


import discord
import requests as r

from sys import exit
from os import system
from json import load, dump
from geopy.geocoders import Nominatim
from pythonping import ping

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
            status = ping("lcroleplay.com", verbose=True)
            if not status:
                await message.channel.send("Website is operational.")
            else:
                await message.channel.send(
                    "Website seems to be having connectivity issues.")

        if message.content.startswith("!weather"):
            locate = "New York City"
            geolocator = Nominatim(
                user_agent=components.user_agent)
            location = geolocator.geocode(locate)
            weather = r.get(components.darksky_line.format(
                location.latitude, location.longitude))
            with open("data/weather.json", "w") as f:
                weather_data = dump(weather.json(), f, indent=4)
            with open("data/weather.json", "r+") as weather:
                weather_data = load(weather)
            await message.channel.send(
                "LC Weather: {}".format(weather_data["currently"]["summary"]
                                        ))


claude = Application()
claude.run(data["token"])
