FROM python:latest


RUN pip install --upgrade pip




# 
RUN pip install psycopg2 && \
    pip install boto3 && \
    pip install notebook && \
    pip install smart_open[all] && \
    pip install google-cloud-storage && \
    pip install pyarrow && \
    pip install nltk && \
    pip install requests && \
    pip3 install minio
    # pip install --upgrade google-cloud-bigquery && \
    # pip install google-cloud-bigquery-storage && \
    # pip install bs4 && \



RUN mkdir -p work/config
WORKDIR /work

RUN mkdir ./packages && \
    export PYTHONPATH="$PWD"

 
#RUN pip install -r ./muAlchemy/requirements.txt

COPY wfunc wfunc
COPY config config
 

RUN pip install --upgrade git+git://github.com/IdontApply/muAlchemy && \
    pip install -e /work/wfunc



RUN pip3 install -r ./wfunc/requirements.txt

COPY /notebooks/. .

