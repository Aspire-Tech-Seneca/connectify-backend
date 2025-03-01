import os
from azure.storage.blob import BlobServiceClient


blob_service_client = BlobServiceClient.from_connection_string("<azure-connection-string>")
container_client = blob_service_client.get_container_client("media")

def upload_profile_image(file_data, filename):
    """
    Uploads the file_data (Bytes) to Azure Blob Storage under the given filename.
    Returns the blob URL on success.
    """
    # Create a blob client
    blob_client = container_client.get_blob_client(blob=filename)

    # Upload the file data
    blob_client.upload_blob(file_data, overwrite=True)
    
    # Construct the blob URL (depending on your account settings)
    return blob_client.url

def delete_profile_image(filename):
    """Deletes a blob from the container."""
    blob_client = container_client.get_blob_client(blob=filename)
    blob_client.delete_blob()

def get_profile_image_url(filename):
    """Get the direct URL of the blob."""
    blob_client = container_client.get_blob_client(blob=filename)
    return blob_client.url
