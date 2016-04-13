from TwitterAPI import TwitterError
import random
import time
import json
import sys
import auth
import psycopg2
import cgi
import urlparse
import os

HEROKU = True

url = "localhost"

if HEROKU:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])


reload(sys)
sys.setdefaultencoding('utf8')

username, password = auth.get_db_credentials()

conn = None
try:
    print "Connecting to PostgreSQL server"
    if HEROKU:
        conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
               )
    else:
        conn = psycopg2.connect("dbname='election_project' user='" + username + "' " +
                                "host='" + url + "' password='" + password + "'")
    print "Connection succeded"
    
except:
    print "Unable to connect to the database"

def save_to_database(data):
    text = data['text'].replace('\'','\'\'').replace('"','""')
    created_at = data['created_at']
    id_str = data['id_str']
    user_id = data['id_str']
    user_name = data['user']['screen_name'].strip("\"")
    coord_str = data['state']
    candidate = data['candidate']
    cur = conn.cursor()

    query = """\
    INSERT INTO twitter_tbl (created_at, id_str, text, user__id_str, user__screen_name, state, candidate)
    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}', '{6}')
    """.format(created_at, id_str, text, user_id, user_name, coord_str, candidate)
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print e
