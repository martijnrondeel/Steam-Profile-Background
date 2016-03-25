from lxml.cssselect import CSSSelector
from urlparse import urlparse
import lxml.html
import urllib2
import cache
import json
import re


def getImage(url):
    """Extracts profile background image URL from inlined CSS property"""
    # Look if we don't already have the image in cache
    cachedResult = cache.lookupSteamID(url)
    if (cachedResult != None) and (cachedResult != "NO_BACKGROUND"):
        return cachedResult
    if cachedResult == "NO_BACKGROUND":
        return None
    content = urllib2.urlopen(url).read()
    tree = lxml.html.fromstring(content)
    elements = tree.cssselect('div.has_profile_background')
    if not elements:
        cache.addSteamID(url, "NO_BACKGROUND", 1)
        return None
    image = elements[0].get("style")
    image = image.replace("background-image: url( '", "")
    image = image.replace("' );", "")
    cache.addSteamID(url, image, 7)
    return image


def getGame(url):
    """Extracts appID from image URL and looks up appID's game name"""
    # Look if we don't already have game in cache
    cachedResult = cache.lookupGame(url)
    if (cachedResult != None) and (cachedResult != "NOT_EXIST"):
        return cachedResult
    if cachedResult == "NOT_EXIST":
        return None
    p = re.compile(ur'\/([0-9]+)\/')
    appID = re.findall(p, url)[0]
    appID = appID.replace("'", "")
    response = urllib2.urlopen(
        "https://store.steampowered.com/api/appdetails?appids=" + appID)
    data = json.load(response)
    if data[appID]["success"] == True:
        name = data[appID]["data"]["name"]
        cache.addGame(url, name, 32)
        return name
    else:
        cache.addGame(url, "NOT_EXIST", 7)
        return None


def invalidURL(url):
    """Checks if URL is faulty"""
    url = urlparse(url)
    if url.netloc == 'steamcommunity.com':
        return False
    else:
        return True
