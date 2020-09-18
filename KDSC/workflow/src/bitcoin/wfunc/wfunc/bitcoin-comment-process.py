import datetime

import nltk
nltk.download('punkt')

import sys
from smart_open import open as sopen
import json
import io


from google.cloud import storage



def cheack_init(row):

    digi=[]
    for token in row:
        
        if any(map(str.isdigit, token)) is True:
            digi.append(token)
    if not digi:
        return None
    else:
        return digi



def get_file_names():
    files = []
    client = storage.Client()
    for blob in client.list_blobs('workflowkddc', prefix='Bitcoin/comments/raw/'):
        files.append(str(blob.name))
    return files


if __name__ == "__main__":


    # path_out = 'gs://workflowkddc/' + sys.argv[1]
    # path_out = sys.argv[1]

    columns_db = [
    'comment_datetime',
    'body',
    'downs',
    'ups',
    'author']
    columns_processed = ['tokens_all_body',
    'poti_digi',
    'created_utc',
    'downs',
    'ups',
    'author']
    columns_gold = [ 'created_utc',
    'dollar_comment',
    'author']

    bucket = 'workflowkddc' 
    prefix = 'Bitcoin/comments' 
    filetype = 'txt'
    filen_procssed = 'processed'
    filen_gold = 'gold'
    filename_procssed = "sliced_comments_tokenized"
    filename_dollar_mention = "dollar_mention"

    path_procssed = 'gs://{}/{}/{}/{}.{}'.format(bucket, prefix, filen_procssed,  filename_procssed, filetype)
    path_gold = 'gs://{}/{}/{}/{}.{}'.format(bucket, prefix, filen_gold,  filename_dollar_mention, filetype)
    # with sopen(path_procssed, 'w') as fout_procssed: 
    with sopen(path_gold, 'w') as fout_gold:
        for path in get_file_names():
            for line in sopen( 'gs://{}/{}'.format(bucket, path), 'rb'): 
                pass
                json_ob = json.loads(line) 

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
                    json_ob_gold = {k: json_ob[k] for k in columns_gold}
                    json.dump(json_ob_gold, fout_gold)
                    fout_gold.write('\n')
   
            









    

