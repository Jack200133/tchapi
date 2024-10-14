import os
import logging
from datetime import datetime as dt
from flask import Blueprint, jsonify  # , make_response
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import json

load_dotenv("./environment/.env")

# Blueprint
geojson_api = Blueprint('geojson_api', __name__)

# Azure Blob Storage configure
LOG_ROUTE = './logs/activity/'
CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "tchgeopandas"  # Replace with your container name
BLOB_NAME = "outputv6.geojson"          # Replace with your blob name

if not os.path.exists(LOG_ROUTE):
    os.makedirs(LOG_ROUTE)

log_filename = LOG_ROUTE + "application_" + \
    dt.now().strftime('%d_%m_%Y') + ".log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_filename), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Endpoint to get the GeoJSON file


@geojson_api.route('/get_geojson', methods=['GET'])
def get_geojson():
    logger.info("Received request to get GeoJSON file.")
    try:
        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(
            CONNECT_STR)
        logger.info("Azure BlobServiceClient created successfully.")

        # Get the BlobClient
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, blob=BLOB_NAME)
        logger.info(
            f"BlobClient for container '{CONTAINER_NAME}'"
            + f" and blob '{BLOB_NAME}' obtained successfully.")

        # Download the blob's content to memory
        downloader = blob_client.download_blob()
        geojson_bytes = downloader.readall()
        logger.info(
            "GeoJSON file downloaded successfully from Azure Blob Storage.")

        # Parse the GeoJSON bytes to a dictionary
        geojson_content = json.loads(geojson_bytes)
        logger.info("GeoJSON content parsed successfully.")

        # Return the GeoJSON content as a JSON response
        return jsonify(geojson_content)

    except Exception as e:
        logger.error(f"Error occurred while fetching GeoJSON file: {str(e)}")
        return jsonify({'error': str(e)}), 500
