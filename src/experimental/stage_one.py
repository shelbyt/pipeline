# from __future__ import print_function
# import boto3
# import os
# import sys
# import uuid
# from PIL import Image
# import PIL.Image
#      
# s3_client = boto3.client('s3')
#      
# def resize_image(image_path, resized_path):
#     with Image.open(image_path) as image:
#         image.thumbnail(tuple(x / 2 for x in image.size))
#         image.save(resized_path)
#      
# def handler(event, context):
#     for record in event['Records']:
#         bucket = record['s3']['bucket']['name']
#         key = record['s3']['object']['key'] 
#         download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
#         upload_path = '/tmp/resized-{}'.format(key)
#         
#         s3_client.download_file(bucket, key, download_path)
#         resize_image(download_path, upload_path)
#         s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)

from __future__ import unicode_literals
import youtube_dl
import boto3
import os

class Logger(object):
        def debug(self, msg):
                pass

        def warning(self, msg):
                print(msg)

        def error(self, msg):
                print(msg)

client = boto3.client('s3')
bucket = 'shelby-lambda-out'

def upload(d):
        filename = "{0}.webm".format(str(d['id']))
        filepath = "/tmp/{0}".format(filename)
        client.upload_file(filepath, bucket, filename)
        client.put_object_acl(ACL='public-read', Bucket=bucket, Key=filename)
        region = "us-west-2"
        return "https://s3-%s.amazonaws.com/{0}/{1}".format(region, bucket, filename)

def processing_hook(d):
        if d['status'] == 'finished':
                print('Done downloading, now converting ...')

def run(event, context):
        url = event['url']
        ydl_opts = {
                'outtmpl': '/tmp/%(id)s.%(ext)s',
                'format': 'bestaudio/best',
                'logger': Logger(),
                'progress_hooks': [processing_hook],
        }

        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
        info = ydl.extract_info(url, True)
        print info

        response = upload(info)
        return { "url" : response }
