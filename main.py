import io
import os
import json
from FollowerCache import FollowerCache
from instagrapi import Client
import time

userDetails = {
    'request2FA': False,
    'username': "",
    'password': "",
}

loginStatus = False

def callAPI(refreshMinutes):
    global code, loginStatus

    if userDetails['request2FA']:
        code = input("Gépeld be kérlek a 2FA Kódot!")

    try:
        cl = Client()
        path = "tmp/" + userDetails['username'] + "-dump.json"
        if os.path.exists(path):
            cl.load_settings(path)

        if not loginStatus:
            cl.login(userDetails['username'], userDetails['password'], False, code)
            loginStatus = True
        else:
            with open(path, 'r') as json_file:
                json_data = json.load(json_file)
                cl.login_by_sessionid(json_data['client_session_id'])

        user_id = cl.user_id_from_username(userDetails['username'])

        if not os.path.exists(path):
            cl.dump_settings(path)

        def compareToOld():
            users = []

            file = open('followers.json')

            users = json.load(file)


            currentCache = FollowerCache(False, users)

            return currentCache

        followers = cl.user_followers(user_id, True, 0)
        cache = FollowerCache(str(followers), False)
        users = cache.getUsers()
        cache.outputUsers()

        print("==================================================")
        print("Differences: ")

        oldCache = compareToOld()
        FollowerCache.outputDifference(oldCache, cache)
        print("==================================================")

        with io.open("followers.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(users))

        cl.logout()
    except Exception as e:
        print(e)
        print("API Hiba!")
        loginStatus = False
        callAPI(refreshMinutes)

    time.sleep(refreshMinutes * 60)
    callAPI(refreshMinutes)

global refreshMinutes

try:
    refreshMinutes = float(input("Milyen gyakorisággal frissüljön az API?"))
except:
    print("Hiba!")

callAPI(refreshMinutes)