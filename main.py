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

        if message.content.startswith("!forum"):
            message_content = str(message.content).replace("!forum",
                                                           "").strip()
            headers = {'XF-Api-Key': '6_O190_vSHsXyo5vcJjU4CwmXRwkukag',
                       'XF-Api-User': "1"}
            params = {'username': message_content}
            forum_data = r.get(
                'http://lcroleplay.com/index.php/api/users/find_name',
                headers=headers, params=params)
            with open("data/forum_profile_data.json", "w+") as f:
                dump(forum_data.json(), f, indent=4)
            with open("data/forum_profile_data.json", "r+") as f:
                temp_data = load(f)
            try:
                username = temp_data["exact"]["username"]
                location = temp_data["exact"]["location"]
                if location == "":
                    location = "(Empty)"
                avatar = str(temp_data["exact"]["avatar_urls"]["m"])
                posts = str(temp_data["exact"]["message_count"])
                embed_profile_data = discord.Embed(
                    title=str(username).replace("(", "").replace(")",
                                                                 "").strip(),
                    color=0x888db5)
                embed_profile_data.set_thumbnail(url=avatar)
                embed_profile_data.add_field(name="Posts", value=str(posts),
                                             inline=False)
                embed_profile_data.add_field(name="Location",
                                             value=str(location).replace("(",
                                                                         "").replace(
                                                 ")", "").strip(),
                                             inline=False)
                await message.channel.send(embed=embed_profile_data)
            except TypeError:
                username = temp_data["recommendations"][0]["username"]
                location = temp_data["recommendations"][0]["location"]
                if location == "":
                    location = "(Empty)"
                avatar = str(
                    temp_data["recommendations"][0]["avatar_urls"]["m"])
                posts = temp_data["recommendations"][0]["message_count"]
                embed_profile_data_2 = discord.Embed(
                    title=str(username).replace("(", "").replace(")",
                                                                 "").strip(),
                    color=0x888db5)
                embed_profile_data_2.set_thumbnail(url=avatar)
                embed_profile_data_2.add_field(name="Posts", value=str(posts),
                                               inline=False)
                embed_profile_data_2.add_field(name="Location",
                                               value=str(location).replace("(",
                                                                           "").replace(
                                                   ")", "").strip(),
                                               inline=False)
                await message.channel.send(embed=embed_profile_data_2)

        if message.content.startswith("!say"):
            content = message.content
            process_message = str(content).replace("!say", "").strip()
            channel = claude.get_channel(657190919535329340)
            await channel.send(process_message)

        if message.content.startswith("!kick"):
            content = message.content
            author = message.author
            channel = claude.get_channel(719624740700160000)
            process_message = str(content).replace("!kick", "").strip()
            if components.check_digits(content):
                try:
                    kick = claude.get_user(int(process_message))
                    await message.guild.kick(kick)
                    await channel.send("kicked {}".format(kick))
                except Exception as e:
                    await message.channel.send(
                        "Failed to kick the user: {}".format(e))
            else:
                await message.channel.send("Error occured. No digits?")


claude = Application()
claude.run(data["token"])
