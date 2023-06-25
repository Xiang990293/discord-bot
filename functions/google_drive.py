from google.cloud import storage
from requests.exceptions import ConnectionError, Timeout
from yt_dlp import YoutubeDL
import yt_dlp
import os
import threading
import json
import urllib
import functions.get_jdata as getj

MODE = 1

jdata = getj.get_jdata(MODE)

PROJECT_ID = jdata['product_id']
BUCKET_NAME = jdata['bucket_name']

STOREAGE_CLASS = 'DURABLE_REDUCED_AVALIBILITY'

def upload_to_gcs(file_data, project_id, bucket_name, filename):
	# Create a Google Cloud Storage client
	storage_client = storage.Client(project=project_id)

	# Get a reference to the storage bucket
	bucket = storage_client.bucket(bucket_name)

	# Upload the file to the bucket
	blob = bucket.blob(filename)
	blob.upload_from_string(file_data, timeout=300, predefined_storage_class=STOREAGE_CLASS)

	# Set the blob's ACL to public-read
	blob.acl.save_predefined("public-read")

	# Get the publicly accessible URL for the file
	url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"

	return url

def download_and_upload(url, options):
	# Download the video
	with YoutubeDL(options) as ydl:
		info_dict = ydl.extract_info(url, download=True)
		filename = ydl.prepare_filename(info_dict)
	return filename, info_dict
	

	
# https://drive.google.com/drive/folders/1eb0873qAzIgmk8bELKKc3GVHtp-CXgzh?usp=sharing