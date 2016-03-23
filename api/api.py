from flask import Flask, request, jsonify
from urlparse import urlparse
from lxml.cssselect import CSSSelector
import lxml.html
import urllib2
import json
import re

app = Flask(__name__)
ssl_cert = ""
ssl_key = ""


def getImage(url):
    """Extracts profile background image URL from inlined CSS property"""
    content = urllib2.urlopen(url).read()
    tree = lxml.html.fromstring(content)
    elements = tree.cssselect('div.has_profile_background')
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


@app.route('/api')
def main():
    data = request.args.get('url', '')
    url = urlparse(data)
    # check if URL is steam profile URL
    if url.netloc == 'steamcommunity.com':
        image = getImage(data)
        game = getGame(image)
        return jsonify(imageURL=image,
                       gameName=game)
    else:
        return "", 404

if __name__ == '__main__':
    app.run('127.0.0.1', debug=False, port=1337,  # API runs behind nginx proxy, so only listen on local
            ssl_context=(ssl_cert, ssl_key), threaded=True)
