from os.path import dirname, join  # realpath,
from os import getcwd
import mualchemy.aualchemy as au

d = getcwd()
# dirname = os.path.dirname
# ++++++++++++++++++++
# d_path =
main_path = dirname(d)
# ++++++++++++++++++++


pdates, search, product, sales, seller , session = au.tables(join(main_path , './config/dbconfig.yaml'))
sellertable = session.query(seller).filter_by(rated = None).first()# clean
s = sellertable# cleab
sellername = s.name
seller_id = s.id

items_list = Pcsv(souce, sellername)
insert_into_seller(session, s, seller_date, item_count)
insert_items(session, seller_id, items_list, sales)
session.commit()