# from minio import Minio
# from minio.error import ResponseError

from os.path import dirname, join  # realpath,
from os import getcwd
import mualchemy.aualchemy as au


# minioClient = Minio('play.min.io',
#                     access_key='Q3AM3UQ867SPQQA43P2F',
#                     secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')


# print(minioClient.bucket_exists('scraper'))





# d = getcwd()
# # dirname = os.path.dirname
# # ++++++++++++++++++++
# # d_path =
# main_path = dirname(d)
# # ++++++++++++++++++++


pdates, search, product, sales, seller , session = au.tables(join())
sellertable = session.query(seller).filter_by(rated = None).first()# clean
s = sellertable# cleab
sellername = s.name
seller_id = s.id
print(s.name)