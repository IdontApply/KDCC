FROM jupyter/base-notebook:python-3.7.6



#COPY requirements.txt .
RUN conda install -c conda-forge voila
RUN conda install geopandas

# RUN mkdir work && \
#     chmod -R 777 /work
# WORKDIR /work
COPY requirements.txt .
# COPY wfunc wfunc
# RUN chmod -R 777 wfunc
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install minio && \
    pip install boto3 && \
    pip install smart_open[all] && \
    pip install google-cloud-storage && \
    pip install pyarrow && \
    pip install nltk
RUN pip install psycopg2-binary

# RUN pip install -r ./wfunc/requirements.txt
# COPY germany germany
# RUN pip install -e wfunc
# # COPY csv csv
COPY ./notebooks/bitcoin.ipynb .
COPY ./notebooks/germanyenergy.ipynb .
COPY ./notebooks/hello.ipynb .

# COPY jupyter_notbook_config.py ./jupyter/jupyter_notbook_config.py

    
