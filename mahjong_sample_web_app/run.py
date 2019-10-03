from pathlib import Path
import json
from mahjong_sample_web_app import app
from mahjong_sample_web_app.config import config
from mahjong_sample_web_app import main  # noqa


def create_app(config_name):
    # app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.logger.debug("Init Flask app config: %s", config_name)
    app.config.from_object(config[config_name])
    # config_json_path = Path(__file__).parent / "config" / "json-schemas"
    # for p in config_json_path.glob("*.json"):
    #     with open(p) as f:
    #         json_name = p.stem
    #         schema = json.load(f)
    #     app.config[json_name] = schema
    #     app.logger.debug("Init json-schema config: %s", config_name)
    return app


if __name__ == "__main__":
    app = create_app("local")  # noqa
    app.run(host="127.0.0.1", port=9080, debug=True)

