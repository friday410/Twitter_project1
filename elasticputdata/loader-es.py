#Import the necessary methods from tweepy library
from pyes import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
#from builtins import print

#Variabl: that contains the user credentials to access Twitter API 
access_token = '931455098-4cheNDFrVVjEqEwyqMEYdIfUznEUP0OZolsGvTeb'
access_token_secret = 'SGJc2RsyyTnhP2RGvLeYniNzRC0sswhxmIIeoaNVsFcoL'
consumer_key = 'jaCwGEBj0rGWkwMqwyGCgfk7q'
consumer_secret = 'joFq8o1BPPIiNmlYMbcZKSa7YcO0W2SspyDagReTsMUfQzRPGK'

conn = None
keywordList = None

class StdOutListener(StreamListener):
	# print 'Getting tweets'
	def on_data(self, data):

		data = json.loads(data)
		
		try:
			if('text' and 'coordinates' in data):
				lo = float(data['coordinates']['coordinates'][0])
				la = float(data['coordinates']['coordinates'][1])

				for word in keywordList:
					if word in data['text']:
						#conn.refresh()
						conn.index({"key":word, "longitude": lo, "latitude": la}, "test-index", "test-type")
		except:
			pass

		return True		
	def on_error(self, status):
		print >> sys.stderr, 'Error with status code:', status_code


if __name__ == '__main__':

	conn = ES('172.31.53.200:9200')

	try:
		conn.indices.delete_index('test-index')
	except:
		pass

	# create an index
	conn.indices.create_index('test-index')

	# initialize a mapping
	mapping = {
		'key': {
			'store':'yes',
			'type': 'string'
		},

		'longitude': {
			'store': 'yes',
			'type':'float'
		},

		'latitude': {
			'store': 'yes',
			'type':'float'
		}
	}

	conn.indices.put_mapping("test-type", {'properties':mapping}, ["test-index"])
	keywordList = ['sunshine','rain','snow','basketball','school','love','music','mountain','happy','sushi']
	#This is a basic listener that just prints received tweets to stdout.

	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	GEOBOX_WORLD = [-130,-60,70,60]
	stream.filter(locations=GEOBOX_WORLD)
	# stream.filter(track=keywordList)
	# stream.filter(track=['sunshine'])
	print('EXECUTED MAIN IN ELASTIC PUT DATA')