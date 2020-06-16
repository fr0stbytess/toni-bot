"""This module acts as our constants, but we
   will call it components.py"""

user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
darksky_line = "https://api.darksky.net/forecast/abe6a84811a8ab8f1f39cd9b8b8f40e1/{},{}"
welcome_line = "Liberty City Roleplay is a medium / heavy English text-only roleplay server which focuses itself on its high standard of roleplay and custom advanced scripts made possible with the help of the Underground Multiplayer mod known as UG:MP. The community consists group of experienced people from all over the world that came from different places and platforms. We are aiming to provide a realistic and enjoyable roleplay environment for all to enjoy and everyone is welcome to come sit down with us and experience what our community has to offer."


def check_digits(s):
    """Check if a string contains digit and return true"""
    return any(i.isdigit() for i in s)
