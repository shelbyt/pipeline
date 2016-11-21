import youtube_dl

class Element:
    def __init(self, name):
        self.name = name

class GCPElement(Element):
    client = boto3.client('s3')

class MSFTElement(Element):
    client = boto3.client('s3')

class AWSElement(Element):
    client = boto3.client('s3')
    bucket = 'shelby-lambda-out'
    region = 'us-west-2'

    def get(self):
        return "%s" % (bucket)

    def put(source,filename):
        client.upload_file(source, bucket, filename)
        client.put_object_acl(ACL='public-read', Bucket=bucket, Key=filename)
        return "https://s3-%s.amazonaws.com/{0}/{1}".format(region, bucket, filename)

    # In AWS a mu worker is a lambda
    def mu(self, lambdas):
        return "NOP"

class BinRunner:
    def __init(self, name):
        self.name = name
    workers = 100
    input = default
    output = default


class ffmpeg_split(Element):
    def mu(self, workers):
        return "ffmpeg -i file.mp4 ffmpeg_temp/%05d.png"


class YDLUploadGeneric(Element):
    def get(yt_url):
        ydl_opts = {
                'outtmpl': '/tmp/%(id)s.%(ext)s',
                'format': 'bestvideo/best',
                'logger': Logger(),
                'progress_hooks': [processing_hook],
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
        info = ydl.extract_info(yt_url, True)

class YDLUpload(AWSElement):
    def get(yt_url):
        ydl_opts = {
                'outtmpl': '/tmp/%(id)s.%(ext)s',
                'format': 'bestvideo/best',
                'logger': Logger(),
                'progress_hooks': [processing_hook],
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
        info = ydl.extract_info(yt_url, True)

yt_mp4 = YDLUpload("From YT").get("www.youtube.com/helloworld")
# In current, are all frames being stored in local tmp directory of lambda?
# What if the size of a worker goes >500mb?
yt_frames = yt_mp4.ffmpeg_spilt("Split frames").mu(1)
yt_frames.put(directory, "myvideo.mp4")

