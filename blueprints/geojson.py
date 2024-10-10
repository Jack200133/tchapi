import os
from flask import Blueprint, jsonify, make_response
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv("../environment/.env")

# Blueprint
geojson_api = Blueprint('geojson_api', __name__)

# Azure Blob Storage configuration
CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "tchgeopandas"  # Replace with your container name
BLOB_NAME = "outputv5.geojson"          # Replace with your blob name

# Endpoint to get the GeoJSON file


@geojson_api.route('/get_geojson', methods=['GET'])
def get_geojson():
    try:
        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(
            CONNECT_STR)

        # Get the BlobClient
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, blob=BLOB_NAME)

        # Download the blob's content to memory
        downloader = blob_client.download_blob()
        geojson_bytes = downloader.readall()

        # Create a response with the GeoJSON content
        response = make_response(geojson_bytes)
        response.headers.set('Content-Type', 'application/geo+json')
        response.headers.set('Content-Disposition',
                             f'attachment; filename={BLOB_NAME}')

        return response

    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500
