import discord
import requests as r

from sys import exit
from os import system
from json import load, dump
from geopy.geocoders import Nominatim

try:
    with open("data/settings.json", "r") as f:
        data = load(f)
except:
    print("Error")


class Application(discord.Client):
    """Core class for core modules managements"""

    async def on_ready(self):
        print("Initialized client as ", self.user)
        try:
            game = discord.Game(data["status"])
            status = discord.Status.idle
            await claude.change_presence(status=status, activity=game)
        except:
            print("something went wrong.")
            exit()


    async def on_message(self, message):
        """Checks if website is operational by pinging it"""
        if message.content.startswith("!status"):
            await message.channel.send("Wait a moment, let me check.")
            status = system("ping lcroleplay.com")
            if not status:
                await message.channel.send("Website is operational.")
            else:
                await message.channel.send(
                    "Website seems to be having connectivity issues.")


    async def on_message(self, message):
        """Retrieve weather info from darksky API"""
        if message.content.startswith("!weather"):
            locate = "New York City"
            geolocator = Nominatim(user_agent="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
            location = geolocator.geocode(locate)
            weather = r.get("https://api.darksky.net/forecast/abe6a84811a8ab8f1f39cd9b8b8f40e1/{},{}".format(location.latitude, location.longitude))
            with open("data/weather.json", "w") as f:
                weather_data = dump(weather.json(), f, indent=4)
            with open("data/weather.json", "r+") as weather:
                weather_data = load(weather)
            await message.channel.send("LC Weather: {}".format(weather_data["currently"]["summary"]))



claude = Application()
claude.run(data["token"])
