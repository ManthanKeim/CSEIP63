from .scraper import get_tweets_max

import os

# register the portals
from sociolyzer import routes
from sociolyzer.routes import app
from sociolyzer.preprocessing import process_text
