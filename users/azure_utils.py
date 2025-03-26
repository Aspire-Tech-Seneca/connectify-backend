import os
import environ

from azure.storage.blob import BlobServiceClient


# Initialize environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
env = environ.Env()
environ.Env.read_env(env_path)

azure_blob = env('AZURE_BLOB_CONNECTION_STRING')
blob_client = BlobServiceClient.from_connection_string(azure_blob)
container_client = blob_client.get_container_client("media")


def upload_image(file_data, filename, folder):
    """
    Uploads the file_data (Bytes) to Azure Blob Storage under the given filename.
    Returns the blob URL on success.
    """
    # Create a blob client
    image_client = container_client.get_blob_client(f"{folder}/{filename}")

    # Upload the file data
    image_client.upload_blob(file_data, overwrite=True)
    
    # Construct the blob URL (depending on your account settings)
    return image_client.url


def delete_image(filename, folder):
    """Deletes a blob from the container."""
    image_client = container_client.get_blob_client(f"{folder}/{filename}")
    image_client.delete_blob()
