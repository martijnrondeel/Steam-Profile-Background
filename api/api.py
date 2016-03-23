from flask import Flask, request, jsonify
from flask_limiter import Limiter
from urlparse import urlparse
from lxml.cssselect import CSSSelector
import lxml.html
import urllib2
import json
import re

app = Flask(__name__)
ssl_cert = ""
ssl_key = ""


def getIP():
    """Returns IP from user behind proxy, needed for rate-limiting"""
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


def invalidURL():
    """Checks if URL is faulty"""
    url = urlparse(request.args.get('url', ''))
    if url.netloc == 'steamcommunity.com':
        return False
    else:
        return True


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

# Enable rate-limiter
limiter = Limiter(
    app,
    key_func=getIP)


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="RATELIMIT_EXCEEDED",
                   description="You exceeded the limit of %s" % e.description), 429


# don't rate limit when URL is invalid
@limiter.limit("200/day;5/minute", exempt_when=incorrectURL)
@app.route('/api')
def main():
    if invalidURL() == False:
        image = getImage(request.args.get('url', ''))
        game = getGame(image)
        return jsonify(imageURL=image, gameName=game)
    else:
        return jsonify(error="INVALID_URL",
                       description="Check if the URL you gave was valid, and the profile is public (example URL: http://steamcommunity.com/id/Martyn96)"), 404


if __name__ == '__main__':
    app.run('127.0.0.1', debug=False, port=1337,  # API runs behind nginx proxy, so only listen on local
            ssl_context=(ssl_cert, ssl_key), threaded=True)
