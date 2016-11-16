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
import sys
import subprocess

class Element:
    def __init__(self,name):
        self.name = name

class Logger(object):
    def debug(self, msg):
            pass

    def warning(self, msg):
            print(msg)

    def error(self, msg):
            print(msg)

client = boto3.client('s3')
#bucket = 'shelby-lambda-out'

# Generic file uploader. Given the bucket name and file
# the contents are uploaded.
def upload(d, bucket, optional=0):
    if optional == 0:
        filename = "{0}.mp4".format(str(d['id']))
        filepath = "/tmp/{0}".format(filename)
        client.upload_file(filepath, bucket, filename)
        client.put_object_acl(ACL='public-read', Bucket=bucket, Key=filename)
        region = "us-west-2"
        return "https://s3-%s.amazonaws.com/{0}/{1}".format(region, bucket, filename)
    if optional == 1:
        for root, dirs, files in os.walk('/tmp/frames/'):
            for file in files:
                print (file)
                client.upload_file(os.path.join(root, file), bucket, file)
                client.put_object_acl(ACL='public-read', Bucket=bucket, Key=file)
        region = "us-west-2"
        return "https://s3-%s.amazonaws.com/{0}".format(region, bucket)

def processing_hook(d):
    if d['status'] == 'finished':
            print('Done downloading, now converting ...')

def split_video(d):
    print ('splitting video start')
    filename = "{0}.mp4".format(str(d['id']))
    filepath = "/tmp/{0}".format(filename)
    split_cmd = 'ffmpeg -i %s'  % (filepath)
    split_cmd += ' -vf fps=1/10 /tmp/frames/%05d.png'
    print (split_cmd)
    output = subprocess.Popen(split_cmd, shell = True, stdout =
            subprocess.PIPE).stdout.read()

    #print subprocess.check_output(["ls, /tmp/"])
    #print subprocess.check_output(["ls, /tmp/frames"])
    print ('splitting video end')
    print(output)
    

# Grab and download a video from a variety of sources
# Problem: What if the video is >500mb?
def load_video(event):
    # source 0 = from s3 bucket
    # source 1 = from url
    if int(event['source']) is 1:
        print ('shelby START\n')
        url = event['url']
        ydl_opts = {
                'outtmpl': '/tmp/%(id)s.%(ext)s',
                'format': 'bestvideo/best',
                'logger': Logger(),
                'progress_hooks': [processing_hook],
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
        info = ydl.extract_info(url, True)
        return info

# Generic operation runner. Give it an input and output along with
# the binary you want to run and options for the binary
def operation(in_loc, out_loc, binary, options):
    print test 


def run(event, context):
    # Clear tmp directory
    subprocess.call(["rm","-rf","/tmp/*"])
    subprocess.call(["mkdir","/tmp/frames"])
    info = load_video(event)
    split_video(info)
    response = upload(info, event['bucket'])
    return { "url" : response }
