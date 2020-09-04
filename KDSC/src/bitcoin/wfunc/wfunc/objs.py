from google.cloud import storage

client = storage.Client()
# https://console.cloud.google.com/storage/browser/[bucket-id]/
bucket = client.get_bucket('workflowkddc')



# Then do other things...
blob = bucket.get_blob('Bitcoin/price/bitstampUSD_1-min_data_2012-01-01_to_2020-04-22.csv'))
# print(blob.download_as_string())
# blob.upload_from_string('New contents!')
# blob2 = bucket.blob('remote/path/storage.txt')
# blob2.upload_from_filename(filename='/local/path.txt')


s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)


from wfunc import db
db = db.Mydatabase()

db.query( """SELECT timeseries.tsm redditsub.body .price_high
                FROM (SELECT tsm FROM timeseries) timeseries
                JOIN ( SELECT tsm, body FROM redditsub WHERE LOWER(body)  SIMILAR TO '% *mo+on *%') redditsub
                ON redditsub.tsm = timeseries.tsm LIMIT(10);

                FROM (SELECT tsm, price_high FROM bitbase ) bitbase
                JOIN (SELECT tsm FROM timeseries) timeseries ON timeseries.tsm = bitbase.tsm

SELECT 
    t.tsm,
    b.price_high,
    t.co
FROM
(SELECT 
    tsm,
    COUNT(*) AS co
FROM
    redditsub
WHERE 
    LOWER(body)  SIMILAR TO '% *mo+on *%'
GROUP BY 
    tsm) t, bitbase b
WHERE
    t.tsm = b.tsm;


SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
FROM   pg_index i
JOIN   pg_attribute a ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
WHERE  i.indrelid = 'timeseries'::regclass
AND    i.indisprimary;

"""