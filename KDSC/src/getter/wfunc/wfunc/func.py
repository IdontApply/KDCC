import requests
import csv
import os
from io import BytesIO

from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
import datetime

# import zstandard as zstd
import json
from smart_open import open as sopen
from smart_open import register_compressor

# from google.cloud import bigquery
import lzma



# minio default secret and access key are used here for simplicity. default secret and access key should be changed and placed as kubernetes secret.
minioClient = Minio('play.min.io',
                access_key='Q3AM3UQ867SPQQA43P2F',
                secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')




    
def dump_prefixed_s3(bucket_minio, bucket_s3, prefix):
    """
    workflow content dump into s3, used at the end of the workflow
    """# TODO decide on a global meaning for prefix, e.g. workflow, notebook or both.


    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_s3)
    
    prefix = prefix +'/'
    # print(minioClient.bucket_exists(bucket))
    # if minioClient.bucket_exists(bucket) is False:
    #     minioClient.make_bucket(bucket)
    try:
        for obj in minioClient.list_objects(bucket_minio, prefix): 
            
            # minioClient.get_object(obj.object_name)
            data = minioClient.get_object(bucket_minio, obj.object_name)
            name = obj.object_name.split('/')[1]
            with open(name, 'wb') as file_data:
                for d in data.stream(32*1024):
                    file_data.write(d)
            bucket.put_object(Key=obj.object_name, Body=open(name, 'rb') )
    except ResponseError as err:
        print(err)
 






def post_notebook(notebook_filename, bucket_name ):
    """
    runs notebook, turns it into html then posts it on public s3
    """

    notebook_ipynb = notebook_filename + '.ipynb'
    notebook_html = notebook_filename + ".html"
    
    with open(notebook_ipynb) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    ep.preprocess(nb, {'metadata': {'path': ''}})

    html_exporter = HTMLExporter()

    html_data, resources = html_exporter.from_notebook_node(nb)

    # with open(notebook_html , "w") as f:
    #     f.write(html_data)
    #     f.close()
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    bucket.put_object(Key=notebook_html, Body=html_data, ContentType='text/html', ACL= 'public-read' )


def save_minio(bucket, key,  prefix):
    """
    saves content to minio. bucket and key should be str
    """# TODO decide on a global meaning for prefix, e.g. workflow, notebook or both.

    print(minioClient.bucket_exists(bucket))
    if minioClient.bucket_exists(bucket) is False:
        minioClient.make_bucket(bucket)
    try:
        with open(key, 'rb') as file_data:
            file_stat = os.stat(key)
            print(minioClient.put_object(bucket, prefix + '/' + key,
                                file_data, file_stat.st_size))
            
    except ResponseError as err:
        print(err)
    print('end of save_minio in')


def get(bucket, urls, prefix):
    """
    downdloads and saves content. bucket is should be a str and urls a dic.
    
    """ # TODO decide on a global meaning for prefix, e.g. workflow, notebook or both.


    print(minioClient.bucket_exists(bucket))
    if minioClient.bucket_exists(bucket) is False:
        minioClient.make_bucket(bucket)
    # https://data.open-power-system-data.org/conventional_power_plants/2018-12-20/conventional_power_plants_DE.csv

    for key in urls: 
        # key
        # a_dict[key]
        with requests.Session() as s:
            with s.get(urls[key], stream=True) as r:
                r.raise_for_status()
                with open(key, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        # decoded_content = chunk.content.decode('utf-8')
                        f.write(chunk)
            
            save_minio( bucket,  key, prefix)
    print('end of get in')

def _handle_xz(file_obj, mode):
    return lzma.LZMAFile(filename=file_obj, mode=mode, format=lzma.FORMAT_XZ)


def get_parse_json_to_gcs(url, bucket, prefix, filetype, filen ='raw'):

    register_compressor('.xz', _handle_xz)

    filename = url.split('/')[-1].split('.')[-2] 
    path = 'gs://{}/{}/{}/{}.{}'.format(bucket, prefix, filen,  filename, filetype)
    with sopen(path, 'wb') as fout: 
        #fout.write(bytes('{', 'utf-8')) 
        for line in sopen(url):
                json_ob = json.loads(line) 
                if json_ob['subreddit'] == 'Bitcoin': 
                    # print(json_ob['body']) 
                    fout.write(bytes(line, 'utf-8'))
    return path











##################################### NOTE END

################# NOTE here is a big query stuff

# def query_big(query):

#     client = bigquery.Client()

#     # Perform a query.

#     query_job = client.query(query)  # API request
#     rows = query_job.result()  # Waits for query to finish
#     return rows

# def download_file(url):
#     local_filename = url.split('/')[-1]
#     # NOTE the stream=True parameter below
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         for line in r.iter_lines(chunk_size=1024*1024, decode_unicode=False, delimiter=None):
#             print(line)
#             with open('gs://my_bucket/my_file.txt', 'wb') as fout:
#                 fout.write(b'hello world')
#             return line

# def stream_pd_minio(bucket, df, filename, prefix):
    
#     path = prefix + '/'  + filename
#     csv_bytes = df.to_csv().encode('utf-8')
#     csv_buffer = BytesIO(csv_bytes)

#     minioClient.put_object(bucket,
#                             path,
#                             data=csv_buffer,
#                             length=len(csv_bytes))

