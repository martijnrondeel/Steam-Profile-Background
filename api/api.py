from flask import Flask, request, jsonify
import ratelimit
import logger
import cache
import tools


app = Flask(__name__)
ssl_cert = ""
ssl_key = ""
limiter = ratelimit.Enable(app)


@app.errorhandler(429)
def ratelimit_handler(e):
    msg = 'User triggered rate-limit ({})'.format(ratelimit.getIP())
    logger.warning(msg, app)
    return jsonify(error="RATELIMIT_EXCEEDED",
                   description="You exceeded the limit of %s" % e.description), 429


@limiter.limit("200/day;10/minute")
@app.route('/api')
def main():
    url = request.args.get('url', '')
    if tools.invalidURL(url) == False:
        image = tools.getImage(url)
        if image == None:
            return jsonify(error="NO_BACKGROUND",
                           description="This Steam profile has no background"), 404
        game = tools.getGame(image)
        return jsonify(imageURL=image, gameName=game)
    else:
        return jsonify(error="INVALID_URL",
                       description="Check if the URL you gave was valid (example URL: http://steamcommunity.com/id/Martyn96)"), 404


if __name__ == '__main__':
    cache.enableCache()
    logger.startLogger(app)
    app.run('127.0.0.1', debug=False, port=1337,  # API runs behind nginx proxy, so only listen on local
            ssl_context=(ssl_cert, ssl_key), threaded=True)
