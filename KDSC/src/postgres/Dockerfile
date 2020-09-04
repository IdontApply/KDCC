FROM postgres:latest

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
#RUN locale-gen en_US.UTF-8
#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8
#ENV LC_CTYPE en_US.UTF-8

COPY initdb/* docker-entrypoint-initdb.d/
COPY db db

# RUN file="$(ls -1 /docker-entrypoint-initdb.d)" && echo $file

