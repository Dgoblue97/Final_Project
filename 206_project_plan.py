## Your name:Daniel Eilender
## The option you've chosen: 2
# Put import statements you expect to need here!

import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import requests_oauthlib
import webbrowser
import requests 


consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

movie_1 = input('Please enter a movie title')
movie_2 = input('Please enter a second movie title')
movie_3 = input('Please enter a third movie title')
movie_data_list =[]

CACHE_FNAME = "SI206_final_project_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()
except:
	CACHE_DICTION = {}


def getwithcaching(movie_title):
	BASE_URL='http://www.omdbapi.com?'
	response = request.get(BASE_URL, params={'t':movie_title})
	if movie_title in CACHE_DICTION_text:
		print 'using cache'
		response_text=CACHE_DICTION_text[movie_title]
	else:
		print 'fetching'
		
		CACHE_DICTION_text[movie_title]= response.text
		response_text=response.text

		cache_file=open(CACHE_FNAME, "w")
		cache_file.write(json.dumps(CACHE_DICTION_text))
		cache_file.close()
	return response_text


a = getwithcaching(movie_1)
movie_data_list.append(a)
b = getwithcaching(movie_2)
c = getwithcaching(movie_3)
movie_data_list.append(b)
movie_data_list.append(c)
# def get_user_tweets(input_word):

# 	unique_identifier = 'twitter_{}'.format(input_word)
# 	if unique_identifier in CACHE_DICTION: # if it is...
# 		return CACHE_DICTION[unique_identifier] # grab the data from the cache!
# 	else:
# 		results = api.search(q = input_word)
# 		CACHE_DICTION[unique_identifier]=results
# 		f=open(CACHE_FNAME, "w")
# 		f.write(json.dumps(CACHE_DICTION, indent = 2))
# 		f.close()
# 		twitter_results = CACHE_DICTION[unique_identifier]
# 		return CACHE_DICTION[unique_identifier]


class Movie():
	def __init__(self, movie_data):
		self.title = movie_data['Title']
		self.release_year = movie_data['Year']
		self.plot = movie_data['Plot']
		self.tomatoMeter = movie_data['tomatoMeter'] 
		self.tomatoUserMeter = movie_data['tomatoUserMeter']
		self.rated = movie_data['Rated'].encode('utf-8')  
		self.id = movie_data['imbdID']
		self.director = movie_data['Director']
		self.imbd_rating = movie_data['imbdRating']

	def rating(self):
		if self.rated =="NC-17":
			return "The rating for " + self.title + " is " + self.rated + ": No One 17 and Under Admitted. Clearly adult. Children are not admitted."
		elif self.rated =='R':
			return "The rating for " + self.title + "is" + self.rated + ": Under 17 requires accompanying parent or adult guardian. Contains some adult material. Parents are urged to learn more about the film before taking their young children with them."
		elif self.rated =="PG-13":
			return "The rating for " + self.title + "is" + self.rated + ": Some material may be inappropriate for children under 13. Parents are urged to be cautious. Some material may be inappropriate for pre-teenagers."
		elif self.rated =="PG":
			return "The rating for " + self.title + "is" + self.rated + ": Some material may not be suitable for children. Parents urged to give 'parental guidance'. May contain some material parents might not like for their young children."
		elif self.rated =="G":
			return "The rating for " + self.title + "is" + self.rated + ": All ages admitted. Nothing that would offend parents for viewing by children."
		else:
			return self.title + " is unrated, viewers should watch at their own discretion."    

	def getMovieAudience(self):
		if self.tomatoMeter > self.tomatoUserMeter:
			return "The Critics like it more"
		elif self.tomatoMeter < self.tomatoUserMeter: 
			return "The Audience likes it more"
		elif self.tomatoMeter == self.tomatoUserMeter:    
			return "Critics and Audience like it the same"
		else:	
			return "Oops thats not a movie!"	
	def movieAppeal(self):
		if self.tomatoMeter + self.tomatoUserMeter > 180:
			return "This movie is very highly acclaimed"
		elif self.tomatoMeter + self.tomatoUserMeter > 140:
			return "This movie was fairly well recieved"	
		elif self.tomatoMeter + self.tomatoUserMeter > 100:
			return "This movie had mixed reviews"
		elif self.tomatoMeter + self.tomatoUserMeter < 100:
			return "This movie was not recieved well"
		else:
			return "Oops, thats not a movie!"					

	def __str__(self):
		return 'The movie {} came out in {}. The plot is: {}'.format(self.title, self.release_year, self.plot)
      
	def num_of_languages(self):
		all_languages = movie_data['Language'].split(",")
		return len(all_languages)
		
list_of_movie_instances = []

first_movie_instance = Movie[movie_data_list[0]]
second_movie_instance = Movie[movie_data_list[1]]
third_movie_instance = Movie[movie_data_list[2]]
list_of_movie_instances.append(first_movie_instance,second_movie_instance,third_movie_instance)







twitter_cache_file = 'twitter_cache_file.json'
try:
	file = open(twitter_cache_file, 'r')
	file_contents = file.read()
	twitter_cache_dictionary = json.loads(file_contents)
else:
	twitter_cache_dictionary = {}
		




# def get_twitter_users(string):
# 	a = re.findall('(?:@)([a-zA-Z0-9_]+)', string)
# 	b = set(a)
# 	return b


































#*****************SQL**************************************************************





conn = sqlite3.connect('Final_Project.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')




table_spec = 'CREATE TABLE IF NOT EXISTS Tweets(tweet_id TEXT PRIMARY KEY, text TEXT, user_id TEXT, title TEXT, favorites INTEGER, retweets INTEGER,)'
cur.execute(table_spec)

table_spec = 'CREATE TABLE IF NOT EXISTS Users(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER,)'
cur.execute(table_spec)

table_spec = 'CREATE TABLE IF NOT EXISTS Movies(movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, num_of_languages INTEGER, imbd_rating INTEGER, top_billed TEXT)'
cur.execute(table_spec)
conn.commit()






# Write your test cases here.

# Attempt is an "instance of a movie"

class Tests(unittest.TestCase):
	def test_1(self):
		self.assertEqual(type(attempt.movieAppeal()), type('a'), "testing type of return value of movieAppeal method in the Movie Class")
	def test_2(self):
		self.assertEqual(attempt.movieAppeal(), 'This movie is very highly acclaimed', 'Testing the return value of movieAppeal method')	
	def test_3(self):
		self.assertEqual(attempt.title, movie_title, 'testting side effect of the consturctor to see if the instance variable is correct')
	def test_4(self):
		self.assertEqual(attempt.rated, "PG", 'Testing the side effect of the constructor to see if if the instance variable self.rated returns the correct rating')
	def test_5(self):
		self.assertEqual(attempt.getMovieAudience(), 'The Audience likes it more', 'Testing the return value of the getMovideAudience method')
	def test_6(self):
		conn = sqlite3.connect('Final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==3,"Testing that there are 3 columns in the Users database")
		conn.close()
	def test_7(self):
		self.assertTrue(Len(list_of_movie_instances) >= 3, 'Testing that the list of Movie instances has 3 or more instances of a movie') 
	def test_8(self):
		conn = sqlite3.connect('Final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[2])==8,"Testing that there are 8 columns in the Movies table")
		conn.close()	

## Remember to invoke all your tests...

unittest.main(verbosity=2) 