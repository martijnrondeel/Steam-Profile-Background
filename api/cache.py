import redis

r = None


def enableCache():
    global r
    r = redis.StrictRedis(host='localhost', port=6379, db=0)


def lookupGame(appID):
    return r.get(appID)


def lookupSteamID(url):
    return r.get(url)


def addGame(appID, gameName, remember):
    r.set(appID, gameName)
    r.expire(appID, remember * 3600)


def addSteamID(url, imageURL, remember):
    r.set(url, imageURL)
    r.expire(url, remember * 3600)
