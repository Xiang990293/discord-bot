from google.cloud import storage
from requests.exceptions import ConnectionError, Timeout
from yt_dlp import YoutubeDL
from google.cloud import storage
import functions.google_drive as fgd
import os
import threading

def upload_file_to_gcs(file_data, project_id, bucket_name, filename):
	# Create a Google Cloud Storage client
	storage_client = storage.Client(project=project_id)

	# Get a reference to the storage bucket
	bucket = storage_client.bucket(bucket_name)

	# Upload the file to the bucket
	blob = bucket.blob(filename)
	blob.upload_from_string(file_data)

	# Set the blob's ACL to public-read
	blob.acl.save_predefined("public-read")

	# Get the publicly accessible URL for the file
	url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"

	return url

async def download_video_and_upload_file_to_gcs(options, url, project_id, bucket_name):
	try:
		with YoutubeDL(options) as ydl:
			info = ydl.extract_info(url, download=True)
			filename = ydl.prepare_filename(info)
			with open(filename, 'rb') as f:
				file_data = f.read()
			url = upload_file_to_gcs(file_data, project_id, bucket_name, f"{info['id']}.{info['ext']}")
			await channel.send(f"Uploaded {info['title']} to Google Cloud Storage: {url}")
	except Exception as e:
		await channel.send(f"Error occurred while downloading/uploading: {e}")
	finally:
		os.remove(filename)
		
	def downloading():
		with YoutubeDL(options) as ydl:
			ydl.download(url)

	download_thread = threading.Thread(target=downloading, args=(url, options))
	download_thread.start()
	
	filename = os.listdir('./temp_file')[0]

	with open(f'temp_file/{filename}', "rb") as f:
		file_data = f.read()
	
	# Create a Google Cloud Storage client
	os.remove(filename)

	
# https://drive.google.com/drive/folders/1eb0873qAzIgmk8bELKKc3GVHtp-CXgzh?usp=sharing