from flask import Flask
from waitress import serve
from blueprints.logger import manage_logger
from blueprints.geojson import geojson_api 
import logging

logging.basicConfig(level=logging.WARNING)

# Flask configuratiosn
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.logger.info('Info level log')
app.logger.warning('Warning level log')
app.logger.error('Error level log')


# Route: /get_metrics
app.register_blueprint(manage_logger)
# Route: /get_geojson
app.register_blueprint(geojson_api)

if __name__ == '__main__':

    serve(app, host="0.0.0.0", port=5000, threads=8)
