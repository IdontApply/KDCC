import requests
import csv
import os

import boto3
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

import zstandard
import lzma

import json

from smart_open import open as sopen
from smart_open import register_compressor

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


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
    downdloads and saves content to minio. bucket is should be a str and urls a dic.
    
    """ # TODO decide on a global meaning for prefix, e.g. workflow, notebook or both.


    print(minioClient.bucket_exists(bucket))
    if minioClient.bucket_exists(bucket) is False:
        minioClient.make_bucket(bucket)
    # https://data.open-power-system-data.org/conventional_power_plants/2018-12-20/conventional_power_plants_DE.csv

    for key in urls: 
        # key
        # a_dict[key]
        with requests.Session() as s:
            download = s.get(urls[key])
            
            decoded_content = download.content.decode('utf-8')
            open(key, 'wb').write(decoded_content.encode("utf-8"))
            
            save_minio( bucket,  key, prefix)
    print('end of get in')



def _handle_xz(file_obj, mode):
    return lzma.LZMAFile(filename=file_obj, mode=mode, format=lzma.FORMAT_XZ)

def _handle_zst(file_obj, mode):
    dctx = zstandard.ZstdDecompressor()
    return dctx.stream_reader(file_obj)



def get_parse_json_to_gcs(url,funcp, bucket, prefix, filetype, filen ='raw'):

    register_compressor('.xz', _handle_xz)
    register_compressor('.zst', _handle_zst)

    filename = url.split('/')[-1].split('.')[-2] 
    path = 'gs://{}/{}/{}/{}.{}'.format(bucket, prefix, filen,  filename, filetype)
    with sopen(path, 'wb') as fout: 
        #fout.write(bytes('{', 'utf-8')) 
        for line in sopen(url):
                json_ob = json.loads(line) 
                if funcp(json_ob): 
                    # print(json_ob['body']) 
                    fout.write(bytes(line, 'utf-8'))
    return path
