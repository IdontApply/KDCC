import datetime

import nltk
nltk.download('punkt')

import sys
from smart_open import open as sopen
import json
import io

import psycopg2
from wfunc import db

from google.cloud import storage

import csv
from io import StringIO

def cheack_init(row):

    digi=[]
    for token in row:
        
        if any(map(str.isdigit, token)) is True:
            digi.append(token)
    if not digi:
        return None
    else:
        return digi




if __name__ == "__main__":


    db = db.Mydatabase()

    # path = 'gs://workflowkddc/' + sys.argv[1]
    path = sys.argv[1]

    columns_db = [
    'comment_datetime',
    'body',
    'downs',
    'ups',
    'author']
    columns_procssed = [ 'created_utc',
    'dollar_comment',
    'author']

    bucket = 'workflowkddc' 
    prefix = 'Bitcoin/comments' 
    filetype = 'txt'
    filen_procssed = 'processed/dollar_mention'
    filename_procssed = path.split('/')[-1].split('.')[-2]


    f = StringIO()
    writer = csv.writer(f,  delimiter ='\t')
    items = []
    path_procssed = 'gs://{}/{}/{}/{}.{}'.format(bucket, prefix, filen_procssed,  filename_procssed, filetype)
    with sopen(path_procssed, 'w') as fout_procssed:
        for line in sopen( 'gs://{}/{}'.format(bucket, path), 'rb'): 
            pass
            json_ob = json.loads(line) 

            value = (int(json_ob['created_utc'])//60*60, repr(json_ob['body']).encode('UTF-8 '), int(json_ob['score']), str(json_ob['author']).encode('UTF-8 ') )
            # items.append(','.join(map(str, value))+'\n')
            writer.writerow(value)
            db.query( "INSERT INTO timeseries VALUES (%s) ON CONFLICT DO NOTHING",parameters = [int(json_ob['created_utc'])//60*60])
            db.commit()

            json_ob['tokens_all_body'] =  nltk.word_tokenize(json_ob['body'])
            json_ob['tokens_digi_body'] = cheack_init(json_ob['tokens_all_body'])
            json_ob['comment_datetime'] = datetime.datetime.fromtimestamp(int(json_ob['created_utc']))

            dollar_list = []
            
            if json_ob['tokens_digi_body']:
                for digi in json_ob['tokens_digi_body']:
                    if digi[0] == "$" or digi[-3:].lower() == 'usd':
                        dollar_list.append(digi)

            json_ob['dollar_comment'] = dollar_list


            if json_ob['dollar_comment']: 
                json_ob_procssed = {k: json_ob[k] for k in columns_procssed}
                json.dump(json_ob_procssed, fout_procssed)
                fout_procssed.write('\n')
   


    
    f.seek(0)
    db.cur.copy_from(f, 'redditsub', columns=('tsm', 'body', 'score', 'author'), sep='\t')
    db.commit()

        
db.close()





    

