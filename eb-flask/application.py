"""
This script runs the TwitterMapProj application using a development server.
"""

from os import environ, system
from datetime import datetime
from flask import render_template, jsonify, Flask
# from TwitterMapProj import app
#from elasticsearch import ElasticSearch
from pyes import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#conn = ES('127.0.0.1:9200')
conn = ES('172.31.53.200:9200')
application = app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""

    return render_template(
        'mainTwitterMap.html',
        title='Main Twitter Map Page',
        year=datetime.now().year,
    )

@app.route('/getTwits/<keyword>')
def get_tweets(keyword):
    keyword = keyword.encode('utf-8')
    data = []
    # SHOULD HERE BE A TIME LIMIT????????
    print 'BEFORE TERM QUERY'
    q = TermQuery('key', keyword)
    print 'AFTER TERM QUERY'
    results = conn.search(query = q)
    print results

    for line in results:
        data.append(line)
        print line
    return jsonify({'data':data})

if __name__ == '__main__':
    # HOST = environ.get('SERVER_HOST', '52.23.164.12')
    # try:
    #     PORT = int(environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    # app.run(HOST, PORT)

    app.run(debug=True, host='0.0.0.0')


