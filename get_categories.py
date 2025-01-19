import os
from functools import lru_cache

from dotenv import load_dotenv
from requests import post

import get_token

env = os.getenv

load_dotenv()
CLIENT_ID = env("CLIENT_ID")
AUTHORIZATION = get_token.authorization()


@lru_cache(maxsize=128)
def category_dict():
    my_dict = {}
    response = post(
        "https://api.igdb.com/v4/genres",
        **{
            "headers": {
                "Client-ID": f"{CLIENT_ID}",
                "Authorization": f"Bearer {AUTHORIZATION}",
            },
            "data": "fields name,id; limit 100;",
        },
    )
    for i in response.json():
        my_dict.update({i["id"]: i["name"]})

    return my_dict


@lru_cache(maxsize=128)
def multiplayer_unique_tags():
    uniqueTags = set()
    uniqueTags.add("Local Coop")
    uniqueTags.add("Online Coop")
    uniqueTags.add("Drop In")
    uniqueTags.add("LAN Coop")
    uniqueTags.add("Split Screen")
    uniqueTags.add("Split Screen Online")
    uniqueTags.add("Local Multiplayer")
    uniqueTags.add("Online Multiplayer")
    uniqueTags.add("4 Players Locally")
    return uniqueTags


@lru_cache(maxsize=128)
def multiplayer_dict(tag_id):
    response = post(
        "https://api.igdb.com/v4/multiplayer_modes",
        **{
            "headers": {
                "Client-ID": f"{CLIENT_ID}",
                "Authorization": f"Bearer {AUTHORIZATION}",
            },
            "data": "fields campaigncoop,dropin,lancoop,offlinecoop,onlinecoop,splitscreen,splitscreenonline; where id = "
            + str(tag_id)
            + ";",
        },
    )

    result = []
    for i in response.json():
        if i.get("offlinecoop"):
            result.append("Local Coop")
        if i.get("onlinecoop"):
            result.append("Online Coop")
        if i.get("dropin"):
            result.append("Drop In")
        if i.get("lancoop"):
            result.append("LAN Coop")
        if i.get("splitscreen"):
            result.append("Split Screen")
        if i.get("splitscreenonline"):
            result.append("Split Screen Online")
        if i.get("offlinemax") and i["offlinemax"] != 0:
            result.append("Local Multiplayer")
        if i.get("onlinemax") and i["onlinemax"] != 0:
            result.append("Online Multiplayer")
        if i.get("offlinemax") and i["offlinemax"] >= 4:
            result.append("4 Players Locally")

    return result
