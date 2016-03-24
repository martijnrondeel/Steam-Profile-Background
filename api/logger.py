from logging.handlers import RotatingFileHandler
from time import gmtime, strftime
import logging


def startLogger(app):
    """Starts the logger"""
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


def warning(msg, app):
    """Add a warning to the log"""
    app.logger.warning('[%s] %s', strftime("%Y-%m-%d %H:%M:%S", gmtime()), msg)
