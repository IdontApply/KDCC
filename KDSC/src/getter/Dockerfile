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


# install selenium
RUN pip install boto3 && \
    pip3 install minio && \
    pip install pyarrow && \
    pip install smart_open[all] && \
    pip install ipython && \
    pip install zstandard
    # pip install selenium
    # pip install zstandard


RUN mkdir -p work
WORKDIR /work

RUN mkdir ./packages && \
    export PYTHONPATH="$PWD"

COPY wfunc wfunc
 
RUN pip install -e /work/wfunc


RUN pip3 install -r ./wfunc/requirements.txt
