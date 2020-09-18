import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import boto3

def post_notebook(notebook_filename, bucket_name ):
    
    notebook_ipynb = notebook_filename + '.ipynb'
    notebook_html = notebook_filename + ".html"

    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})

    html_exporter = HTMLxporter()

    html_data, resources = html_exporter.from_notebook_node(nb)

    with open(notebook_html , "wb") as f:
        f.write(html_data)
        f.close()
    

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(notebook_html, notebook_html, ExtraArgs={'ACL':'public-read'})
