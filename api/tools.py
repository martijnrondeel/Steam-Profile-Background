from lxml.cssselect import CSSSelector
from urlparse import urlparse
import lxml.html
import urllib2
import json
import re


def getImage(url):
    """Extracts profile background image URL from inlined CSS property"""
    content = urllib2.urlopen(url).read()
    tree = lxml.html.fromstring(content)
    elements = tree.cssselect('div.has_profile_background')
    if not elements:
        return None
    url = elements[0].get("style")
    url = url.replace("background-image: url( '", "")
    url = url.replace("' );", "")
    return url


def getGame(url):
    """Extracts appID from image URL and looks up appID's game name"""
    p = re.compile(ur'\/([0-9]+)\/')
    appID = re.findall(p, url)[0]
    appID = appID.replace("'", "")
    response = urllib2.urlopen(
        "https://store.steampowered.com/api/appdetails?appids=" + appID)
    data = json.load(response)
    return data[appID]["data"]["name"]


def invalidURL(url):
    """Checks if URL is faulty"""
    url = urlparse(url)
    if url.netloc == 'steamcommunity.com':
        return False
    else:
        return True
