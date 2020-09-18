FROM python:latest
# update apk repo #FROM python:alpine #1
# RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
#     echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# install chromedriver
# RUN apk update && \
#     apk add chromium chromium-chromedriver && \
#     apk add postgresql-dev && \
#     apk add gcc && \
#     apk --update add python3-dev && \
#     apk add musl-dev && \
#     apk --update add git less openssh && \
#     rm -rf /var/lib/apt/lists/* && \
#     rm /var/cache/apk/*
# upgrade pip
RUN pip install --upgrade pip
RUN pip install geopandas

# install selenium
RUN pip install selenium && \
    pip install psycopg2 && \
    pip install bs4 && \
    pip install boto3 && \
    pip install google-cloud-storage && \
    pip install notebook && \
    pip install zstandard
# RUN git clone git://github.com/pallets/jinja.git && \
#     cd jinja2 && \
#     python setup.py develop

RUN mkdir -p work/config
WORKDIR /work

RUN mkdir ./packages && \
    export PYTHONPATH="$PWD"

 
#RUN pip install -r ./muAlchemy/requirements.txt

COPY wfunc wfunc
COPY config config
 
# COPY ./test.py .
# CMD ['python3','test.py']  
RUN pip3 install --upgrade git+git://github.com/IdontApply/muAlchemy && \
    pip3 install minio && \
    pip install -e /work/wfunc
   
RUN pip3 install git+git://github.com/IdontApply/muscraper
RUN pip3 install -r ./wfunc/requirements.txt

COPY /notebooks/. .
#RUN git clone https://github.com/IdontApply/Dbtools
