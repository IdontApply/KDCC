FROM python:alpine

# update apk repo
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update && \
    apk add chromium chromium-chromedriver && \
    apk add postgresql-dev && \
    apk add gcc && \
    apk --update add python3-dev && \
    apk add musl-dev && \
    apk --update add git less openssh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/*
# upgrade pip
RUN pip install --upgrade pip

# install selenium
#RUN pip install selenium
RUN pip install psycopg2



RUN mkdir -p work/config
WORKDIR /work
RUN mkdir ./packages


#RUN pip install -r ./muAlchemy/requirements.txt
COPY wfunc wfunc
COPY config config
# COPY ./test.py .
# CMD ['python3','test.py']
RUN pip3 install --upgrade git+git://github.com/IdontApply/muAlchemy && \
    git clone https://github.com/IdontApply/muscraper -b development && \
    pip3 install minio
#RUN git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
