"""This is the core file of our Discord bot
   Claude."""

import json
import discord
import requests as r
import mysql.connector as connector

from geopy.geocoders import Nominatim
from modules import components

try:
    with open("data/settings.json", "r") as f:
        data = json.load(f)
except Exception as e:
    print("Error:", e)

try:
    connection = connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="lcrp")
    cursor = connection.cursor()
    print("Connection to the database succesfully established.")
except Exception as e:
    print("Connection to the database failed: .", e)




intents = discord.Intents.default()
intents.members = True


class Application(discord.Client):
    """Core class for core processing"""

    async def on_ready(self):
        print("Initialized client as: ", self.user)
        try:
            game = discord.Game(data["default_activity"])
            status = discord.Status.idle
            await toni.change_presence(status=status, activity=game)
        except Exception as e:
            print("something went wrong:", e)
            exit()

    async def on_message(self, message):
        if message.content.startswith("!status"):
            await message.channel.send("Wait a moment, let me check.")
            try:
                r.get("https://lcroleplay.com/index.php", verify=False)
                await message.channel.send("Website is on and working fine.")
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
                json.dump(weather.json(), f, indent=4)
            with open("data/weather.json", "r+") as weather:
                weather_data = json.load(weather)
            await message.channel.send(
                "Current Liberty City weather: {}".format(
                    weather_data["currently"]["summary"]
                ))

        if message.content.startswith("!activity"):
            activity = str(message.content).replace("!activity", "").strip()
            author = str(message.author)
            channel_id = toni.get_channel(788941431279845440)
            with open("data/settings.json", "r") as f:
                data = json.load(f)
                data["last_activity"] = activity
            with open("data/settings.json", "w") as f:
                json.dump(data, f, indent=4)
            with open("data/settings.json", "r") as f:
                data = json.load(f)
                for perm in data["perms"]:
                    if perm in author:
                        status = discord.Status.idle
                        activity = discord.Game(data["last_activity"])
                        await toni.change_presence(status=status,
                                                     activity=activity)
                        await channel_id.send(
                            "New activity: `{}`. Edited by: `{}`".format(
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
                json.dump(forum_data.json(), f, indent=4)
            with open("data/forum_profile_data.json", "r+") as f:
                temp_data = json.load(f)
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
            channel = toni.get_channel(657190919535329340)
            await channel.send(process_message)

        if message.content.startswith("!approve"):
            content = message.content
            author = message.author
            process_message = str(content).replace("!approve", "").strip()
            approved_channel_log = toni.get_channel(797577949104439327)
            try:
                approval_query = "UPDATE samp_users SET activated = '1' WHERE samp_users.user = '" + str(process_message)+"'"
                cursor.execute(approval_query)
                await approved_channel_log.send("{} has been approved by staff member {}".format(process_message, author))
                connection.commit()
            except Exception as e:
                await approved_channel_log.send("Could not approve the member! Error: {}".format(e))

        if message.content.startswith("!kick"):
            content = message.content
            author = message.author
            channel = claude.get_channel(657190919535329340)
            process_message = str(content).replace("!kick", "").strip()
            if components.check_digits(content):
                try:
                    kick = claude.get_user(int(process_message))
                    await message.guild.kick(kick)
                    await channel.send(
                        "KICK LOG: {} was kicked by: {}.".format(kick, author))
                except Exception as e:
                    await message.channel.send(
                        "Error kicking the user: {}.".format(e))
            else:
                await message.channel.send("Error occured. No digits?")

        keywords = ["Null", "Nulled"]
        for keyword in keywords:
            if message.content.startswith(str(keyword)):
                await message.channel.send("Woah, what?")

    async def on_member_join(self, member):
        member = member
        logs_channel = toni.get_channel(788941431279845440)
        embed = discord.Embed(title="Welcome to Liberty City Roleplay!")
        embed.add_field(name="What is Liberty City Roleplay?",
                        value=str(components.welcome_line), inline=False)
        embed.add_field(name="Forums",
                        value="https://lcroleplay.com/", inline=False)
        try:
            await member.send(embed=embed)
            await logs_channel.send("Welcome message succesfully sent to: {}"
                                    "".format(member))
        except Exception as e:
            await logs_channel.send("Failed to send the message: {}".format(e))


toni = Application(intents=intents)
toni.run(data["token"])
