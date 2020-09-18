import requests
import csv
import os

import boto3
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


# minio default secret and access key are used here for simplicity. default secret and access key should be changed and placed as kubernetes secret.
minioClient = Minio('play.min.io',
                access_key='Q3AM3UQ867SPQQA43P2F',
                secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')


# FIXME

def dump_prefixed_s3(bucket, prefix):
    """
    workflow content dump into s3, used at the end of the workflow
    """

    print(minioClient.bucket_exists(bucket))
    if minioClient.bucket_exists(bucket) is False:
        minioClient.make_bucket(bucket)
    try:
        for object in minioClient.list_objects_v2(bucket, prefix):
            object.object_name()
            minioClient.get_object(object.object_name())
            
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





def save_minio(bucket, key):
    """
    saves content to minio. bucket and key should be str
    """
    print(minioClient.bucket_exists(bucket))
    if minioClient.bucket_exists(bucket) is False:
        minioClient.make_bucket(bucket)
    try:
        with open(key, 'rb') as file_data:
            file_stat = os.stat(key)
            print(minioClient.put_object(bucket, key,
                                file_data, file_stat.st_size))
    except ResponseError as err:
        print(err)

def get(bucket, urls):
    """
    downdloads and saves content. bucket is should be a str and urls a dic.
    """
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
            
            save_minio( bucket, key)


