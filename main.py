"""This is the core file of our Discord bot
   Claude."""

from json import load, dump
from sys import exit

import discord
import requests as r
from geopy.geocoders import Nominatim

from modules import components

try:
    with open("data/settings.json", "r") as f:
        data = load(f)
except Exception:
    print("Error:", Exception)


class Application(discord.Client):
    """Core class for core processing"""

    async def on_ready(self):
        print("Initialized client as ", self.user)
        try:
            game = discord.Game(data["default_activity"])
            status = discord.Status.idle
            await claude.change_presence(status=status, activity=game)
        except Exception:
            print("something went wrong:", Exception)
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

        if message.content.startswith("!activity"):
            activity = str(message.content).replace("!activity", "").strip()
            author = str(message.author)
            channel_id = claude.get_channel(719624740700160000)
            with open("data/settings.json", "r") as f:
                data = load(f)
                data["last_activity"] = activity
            with open("data/settings.json", "w") as f:
                dump(data, f, indent=4)
            with open("data/settings.json", "r") as f:
                data = load(f)
                for perm in data["perms"]:
                    if perm in author:
                        status = discord.Status.idle
                        activity = discord.Game(data["last_activity"])
                        await claude.change_presence(status=status,
                                                     activity=activity)
                        await channel_id.send(
                            "New activity set to: `{}`. Updated by `{}`".format(
                                activity, author))


claude = Application()
claude.run(data["token"])
