FROM google/cloud-sdk:alpine
RUN apk --no-cache add postgresql-client
RUN touch ~/.pgpass
RUN chmod 0600 ~/.pgpass
COPY backup.sh .
ENTRYPOINT [ "psql" ]