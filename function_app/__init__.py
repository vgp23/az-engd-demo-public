import azure.functions as func
import logging
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# ---------------------------
# HTTP trigger: simple hello
# ---------------------------
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = req_body.get('name') if req_body else None

    if name:
        return func.HttpResponse(f"Hello, {name}. HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "HTTP triggered function executed successfully. Pass a name in the query string or request body.",
            status_code=200
        )


# ---------------------------
# Blob trigger: logs blob info
# ---------------------------
@app.blob_trigger(arg_name="myblob", path="victorcontainer",
                  connection="BlobStorageConnectionString")
def BlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger processed blob. Name: {myblob.name}, Size: {myblob.length} bytes")


# ---------------------------
# Helper for reading blob safely
# ---------------------------
def read_blob(blob_name: str) -> bytes:
    account_url = os.environ.get("BLOB_STORAGE_ACCOUNT_URL")
    if not account_url:
        logging.warning("BLOB_STORAGE_ACCOUNT_URL not set; returning empty content for testing")
        return b""

    token_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=token_credential)
    blob_client = blob_service_client.get_blob_client(container="victorcontainer", blob=blob_name)
    return blob_client.download_blob().readall()


# ---------------------------
# HTTP trigger: read blob
# ---------------------------
@app.route(route="readblob", auth_level=func.AuthLevel.ANONYMOUS)
def http_read_blob(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger 'readblob' processing request")

    blob_name = req.params.get("file")
    if not blob_name:
        return func.HttpResponse("Please pass a 'file' name in the query string", status_code=400)

    try:
        blob_data = read_blob(blob_name)
        return func.HttpResponse(blob_data, mimetype="application/octet-stream")
    except Exception as e:
        logging.error(f"Failed reading blob: {e}")
        return func.HttpResponse(f"Failed to read blob: {str(e)}", status_code=500)
