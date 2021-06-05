from .scraper import get_tweets_max

import os

# register the portals
from twitterdash import routes
from twitterdash.routes import app
from twitterdash.preprocessing import process_text
