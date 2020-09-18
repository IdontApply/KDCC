import requests
import csv
import os
from io import BytesIO

import boto3

import datetime

import pandas as pd
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
# from google.cloud import bigquery

# import zstandard as zstd
import requests





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








# FIXME

# def query_big(query):

#     client = bigquery.Client()

#     # Perform a query.

#     query_job = client.query(query)  # API request
#     rows = query_job.result()  # Waits for query to finish
#     return rows






            