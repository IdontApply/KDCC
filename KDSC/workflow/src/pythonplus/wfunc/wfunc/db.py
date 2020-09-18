import psycopg2
from os import getenv

class Mydatabase():
    """
    database class for a connection instance     
    """
    def __init__(self, user = getenv('POSTGRES_USER'), host = getenv('POSTGRES_HOST'),
     password = getenv('POSTGRES_PASSWORD'), db = getenv('POSTGRES_DATABASE'), port = getenv('POSTGRES_PORT')): # todo config host in the config
        
        self.conn = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def query(self, query, parameters = None):
        self.cur.execute(query, parameters)

    def copy_from_file(self,  file, table, columns):
        """
        use copy_from() to copy it to the table
        """
        try:
            self.cur.copy_from(file, table, columns=columns)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            self.cur.close()
            return 1

    def fetch1(self):
        return self.cur.fetchone()[0]

    def fetcha(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()

    def cr(self):
        return self.cur

    def conn(self):
        return self.conn

    def commans(self):
        '''
        add quries here for re-use
        '''
        list_queries = [
        ]
        return list_queries
