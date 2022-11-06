import json


class FollowerCache:
    def __init__(self, data, users):
        if data:
            self.data = data
            users = []

            start = 0
            while True:
                start1 = data.find("username", start)
                start2 = data.find("full_name", start)

                start = start2 + 9

                if start2 == -1:
                    break
                else:
                    num1 = (start1 + 10)
                    num2 = (start2 - 3)
                    username = data[num1:num2]

                    users.append(username)

            users.sort()
            self.users = users

        if users:
            self.data = ""
            self.users = users

    def outputData(self):
        print(self.data)

    def getUsers(self):
        return self.users

    def outputUsers(self):
        for username in self.users:
            print(username)

    @classmethod
    def compare(cls, obj1, obj2):
        if obj1 and obj2:
            if type(obj1) == type(obj2):
                return obj1.users == obj2.users

    @classmethod
    def userDifference(cls, obj1, obj2):
        if obj1 and obj2:
            if type(obj1) == type(obj2):
                return list(set(obj1.users) - set(obj2.users))

    @classmethod
    def outputDifference(cls, obj1, obj2):
        users = []

        if len(obj1.users) > len(obj2.users):
            users = list(set(obj1.users) - set(obj2.users))
        else:
            users = list(set(obj2.users) - set(obj1.users))

        for username in users:
            print(username + " >> " + ((username in obj2.users) and "Followed" or "Unfollowed"))