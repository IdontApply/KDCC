# from minio import Minio
# from minio.error import ResponseError

from os.path import dirname, join  # realpath,
from os import getcwd
import mualchemy.aualchemy as au
from sescrp import getter
from selenium.webdriver.support import expected_conditions as ec
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


def scrap_seller():

    pdates, search, product, sales, seller ,session = au.tables()
    sellertable = session.query(seller).filter_by(rated = None).first()# clean
    s = sellertable# cleab
    # sellername = s.name
    # seller_id = s.id
    #  # cleab

    # if s.name == 'souq-shop':
    #     s.rated = False
    #     session.commit()
    #     exit()

    sellername = s.name
    seller_id = s.id


    try:
        souce, seller_date, item_count = getter.html_getter(sellername)
        print('gotsouce')

    except ec.NoSuchElementException:
        print('nosales')
        s.rated = False
        session.commit()
        
        exit()