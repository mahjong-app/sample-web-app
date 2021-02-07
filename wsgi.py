import os
import logging
from mahjong_sample_web_app.run import create_app


if os.environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
app = create_app("local")
