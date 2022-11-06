import io
import json
from FollowerCache import FollowerCache
from instagrapi import Client

cl = Client()
cl.load_settings('tmp/dump.json')
cl.login("username", "password", True, "2fa")
user_id = cl.user_id_from_username("username")

#TODO: First usenál nézze meg létezik-e a fájl, ha létezik töltse be ha nem hozza létre és a fájlt resettelje ha nem tud beloginolni.

def compareToOld():
    users = []

    try:
        file = open('followers.json')

        users = json.load(file)
    except:
        break


    currentCache = FollowerCache(False, users)

    return currentCache

followers = cl.user_followers(user_id, True, 0)
cache = FollowerCache(str(followers), False)
users = cache.getUsers()

oldCache = compareToOld()
FollowerCache.outputDifference(oldCache, cache)



#TODO: x időnként kérje le a followereket és ha lekérte akkor checkelje, hogy az oldFollowerek között mi a változás, ha van.
with io.open("followers.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(users))