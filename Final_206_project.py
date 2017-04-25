## Your name:Daniel Eilender
## The option you've chosen: 2
# Put import statements you expect to need here!
###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.

# Begin filling in instructions....
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import requests 
from pprint import pprint

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

movie_1 = 'Gladiator'
movie_2 = 'Hoosiers'
movie_3 = 'Avatar'
movie_list = [] # making a list of movie titles
movie_list.append(movie_1)
movie_list.append(movie_2)
movie_list.append(movie_3)


CACHE_FNAME = "SI206_final_project_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


def getwithcaching(movie_title): # function to either get movie data from cache or requests movie adata using title
	BASE_URL='http://www.omdbapi.com?'
	if movie_title in CACHE_DICTION:
		# print ('using cache')
		response_text=CACHE_DICTION[movie_title]
	else:
		# print ('fetching')
		response = requests.get(BASE_URL, params={'t':movie_title})
		CACHE_DICTION[movie_title] = response.text
		response_text = response.text
		
		# print (type(response_text))
		cache_file = open(CACHE_FNAME, "w")
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return (json.loads(response_text))

movie_data_list =[] # Making a list of movie data dictionarys
for movie in movie_list:
	data = getwithcaching(movie)
	movie_data_list.append(data)

# print (movie_data_list[0])
# for movie in movie_data_list:
# 	print (movie_data_list)
# def get_user_tweets(input_word):



class Movie(object): # Movie class that pulls data from movie dictionaries when making an instance
	def __init__(self, movie_data):
		self.title = movie_data['Title']
		self.release_year = movie_data['Year']
		self.plot = movie_data['Plot']
		self.tomatoCriticMeter_string = movie_data["Metascore"]
		self.tomatoCriticMeter = int(self.tomatoCriticMeter_string) 
		self.tomatoUserMeter_string = movie_data['Ratings'][1]['Value'][:1]
		self.tomatoUserMeter = int(self.tomatoUserMeter_string)
		self.rated = movie_data['Rated']# .encode('utf-8') 
		self.id = movie_data['imdbID']
		self.director = movie_data['Director']
		self.imdb_rating_string = (movie_data['imdbRating'])
		self.imdb_rating = float(self.imdb_rating_string)
		self.movie_data = movie_data
		
	def rating(self):
		if self.rated =="NC-17":
			return "The rating for " + self.title + " is " + self.rated + " : No One 17 and Under Admitted. Clearly adult. Children are not admitted."
		elif self.rated =='R':
			return "The rating for " + self.title + " is " + self.rated + " : Under 17 requires accompanying parent or adult guardian. Contains some adult material. Parents are urged to learn more about the film before taking their young children with them."
		elif self.rated =="PG-13":
			return "The rating for " + self.title + " is " + self.rated + " : Some material may be inappropriate for children under 13. Parents are urged to be cautious. Some material may be inappropriate for pre-teenagers."
		elif self.rated =="PG":
			return "The rating for " + self.title + " is " + self.rated + " : Some material may not be suitable for children. Parents urged to give 'parental guidance'. May contain some material parents might not like for their young children."
		elif self.rated =="G":
			return "The rating for " + self.title + " is " + self.rated + " : All ages admitted. Nothing that would offend parents for viewing by children."
		else:
			return self.title + " is unrated, viewers should watch at their own discretion."    

	def getMovieAudience(self):
		if self.tomatoCriticMeter > self.tomatoUserMeter:
			return "The Critics like it more"
		elif self.tomatoCriticMeter < self.tomatoUserMeter: 
			return "The Audience likes it more"
		elif self.tomatoCriticMeter == self.tomatoUserMeter:    
			return "Critics and Audience like it the same"
		else:	
			return "Oops thats not a movie!"	
	def movieAppeal(self):
		if self.tomatoCriticMeter + self.tomatoUserMeter > 180:
			return "This movie is very highly acclaimed"
		elif self.tomatoCriticMeter + self.tomatoUserMeter > 140:
			return "This movie was fairly well recieved"	
		elif self.tomatoCriticMeter + self.tomatoUserMeter > 100:
			return "This movie had mixed reviews"
		elif self.tomatoCriticMeter + self.tomatoUserMeter < 100:
			return "This movie was not recieved well"
		else:
			return "Oops, thats not a movie!"					
      
	def num_of_languages(self):
		all_languages = self.movie_data['Language'].split(',')
		return len(all_languages)
	def get_actors(self):
		list_of_actors = self.movie_data['Actors'].split(',')
		return str(list_of_actors)
	def top_actor(self):
		list_of_actors = self.movie_data['Actors'].split(',')
		return list_of_actors[0]		


list_of_movie_instances = []

for movie in movie_data_list: # Using a for loop to run each movie dictionary into the class Movie and make an instance. Then appending these instances into a list
	movie_instance = Movie(movie)
	list_of_movie_instances.append(movie_instance)


movie_tuple_list = []

for movie_instance in list_of_movie_instances: # This block of code is creating a list of three movie tuples containing data on three different movies
	new_tuple = (movie_instance.id, movie_instance.title, movie_instance.plot, movie_instance.rated, movie_instance.director, movie_instance.imdb_rating, movie_instance.num_of_languages(), movie_instance.get_actors(), movie_instance.getMovieAudience(), movie_instance.rating(), movie_instance.top_actor())
	movie_tuple_list.append(new_tuple)
		



#************TWITTER**************************************************************


twitter_cache_file = 'twitter_cache_file2.json'
try:
	file = open(twitter_cache_file, 'r')
	file_contents = file.read()
	twitter_cache_dictionary = json.loads(file_contents)
except:
	twitter_cache_dictionary = {}


def get_tweetdata_with_caching(input_word):

	unique_identifier = input_word
	if unique_identifier in twitter_cache_dictionary: # if it is...
		twitter_results = twitter_cache_dictionary[unique_identifier]
		# print('using twitter cache') # grab the data from the cache!
		return twitter_results['statuses']
	else:
		twitter_results = api.search(q = unique_identifier, count = 50)
		# print ('fetching twitter data')
		twitter_cache_dictionary[unique_identifier] = twitter_results
		f=open(twitter_cache_file, "w")
		f.write(json.dumps(twitter_cache_dictionary))
		f.close()
		
		return twitter_results['statuses']


List_twitter_search_Directors = [] # Getting the Directors of three movies from the list of movie instances
for instance in list_of_movie_instances:
	director = instance.director
	List_twitter_search_Directors.append(director)


# print (List_twitter_search_Directors)
List_of_twitter_data_list = [] # Getting twitter data from either a cache or API by searching by Director name
for search_term in List_twitter_search_Directors:
	# print (search_term)
	# print ("search term is above")

	data = get_tweetdata_with_caching(search_term)

	List_of_twitter_data_list.append(data)
# print(type(List_of_twitter_data_list[0][0]))
# print (List_of_twitter_data_list)
class Tweet(object): # a class to pull out data from a list of twitter data, input is a list
		def __init__(self, tweets): # tweets represents one tweet dictionary
			# for tweets in tweet_data: 
			self.tweet_id = tweets['id_str']
			self.text = tweets['text']
			self.user_id = tweets['user']['id_str']
			self.favorites = tweets['favorite_count']
			self.retweets = tweets['retweet_count']
			self.movie_id = ''
			self.screen_name = tweets['user']['screen_name']

			self.user_mentions = tweets['entities']['user_mentions']
			self.user_screenames = []
			self.search_term = ''
			for term in list_of_movie_instances:
				if term.title.lower() in self.text:
					self.movie_id = term.id
				elif term.title in self.text:
					self.movie_id = term.id
				elif term.title.upper() in self.text:
					self.movie_id = term.id
			for users in self.user_mentions:
				self.user_screenames.append(users['screen_name'])
			for term in List_twitter_search_Directors:
				if term in self.text:
					self.search_term = term

			# need to get users mentioned from these tweets
			
				
List_of_tweet_instances = []




for data in List_of_twitter_data_list:
	for single_tweet in data: # list of twitter data list is alist of list
		instance = Tweet(single_tweet)
		# print (instance.user_screenames)
		List_of_tweet_instances.append(instance)
List_of_tweet_tuples = []
Screennames_list = []
for instance in List_of_tweet_instances:
	new_tuple = (instance.tweet_id, instance.text, instance.user_id, instance.favorites, instance.retweets, instance.movie_id, instance.search_term)	
	List_of_tweet_tuples.append(new_tuple)
	Screennames_list.append(instance.screen_name)
	if instance.user_screenames != []:
		for single_name in instance.user_screenames:
			Screennames_list.append(single_name)
# print (Screennames_list)		
	
# Put data into a list of tuples

# Then insert this data into Tweets Table



#***********USERS*****************************************************************


CACHE_FNAME = "twitter_user_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


# Define your function get_user_tweets here:

def get_user_tweets_information(input_word):

	unique_identifier = input_word
	if unique_identifier in CACHE_DICTION: # if it is...
		return CACHE_DICTION[unique_identifier] # grab the data from the cache!
	else:
		results = api.get_user(input_word)
		CACHE_DICTION[unique_identifier]=results
		f=open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION, indent = 2))
		f.close()
		twitter_results = CACHE_DICTION[unique_identifier]
		return CACHE_DICTION[unique_identifier]




class TweetUser(object): # a class to pull out data from a list of twitter data, input is a list
		def __init__(self, tweets):
			# print (type(tweets))
			# print (tweet_data)
			self.tweet_id = tweets['id_str']
			
			self.user_id = tweets['user']['id_str']
			self.favorite_count = tweets['user']['favourites_count']
			self.num_of_followers = tweets['user']['followers_count']
			self.tweet_count = tweets['user']['statuses_count']
			self.screen_name = tweets['user']['screen_name']
			self.location = tweets['user']['location']
			self.num_of_following = tweets['user']['friends_count']

User_data_list = []
for screen_name in Screennames_list:
	data = get_user_tweets_information(screen_name)
	User_data_list.append(data)
# print (User_data_list[0])	

List_of_tweet_User_instances = []

for data in List_of_twitter_data_list:
	for single_user_tweet in data:
		instance = TweetUser(single_user_tweet)
		List_of_tweet_User_instances.append(instance)

List_of_tweet_user_tuples = []

for instance in List_of_tweet_User_instances:
	new_tuple = (instance.user_id, instance.screen_name, instance.favorite_count, instance.num_of_followers, instance.num_of_following, instance.tweet_count, instance.location)	
	List_of_tweet_user_tuples.append(new_tuple)









#*****************SQL**************************************************************





conn = sqlite3.connect('Final_Project.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')



table_spec = 'CREATE TABLE IF NOT EXISTS Tweets(tweet_id TEXT PRIMARY KEY, text TEXT, user_id TEXT, favorites INTEGER, retweets INTEGER, movie_id TEXT, search_term TEXT)'
cur.execute(table_spec)
# Need to add title TEXT to Tweets


table_spec = 'CREATE TABLE IF NOT EXISTS Users(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER, num_followers INTEGER, num_following INTEGER, num_tweets INTEGER, location TEXT)'
cur.execute(table_spec)

	


table_spec = 'CREATE TABLE IF NOT EXISTS Movies(Movie_id TEXT PRIMARY KEY, Title TEXT, Plot TEXT, Rated TEXT, Director TEXT, imdb_rating INTEGER, num_of_languages INTEGER, Actors TEXT, Audience TEXT, Rating TEXT, Top_Actor TEXT)'
cur.execute(table_spec)
conn.commit()

statement = 'INSERT OR IGNORE INTO Movies Values (?,?,?,?,?,?,?,?,?,?,?)'
for movie in movie_tuple_list:
	cur.execute(statement, movie)
conn.commit()	


statement_2 = 'INSERT OR IGNORE INTO Tweets Values (?,?,?,?,?,?,?)'
for tweet in List_of_tweet_tuples:
	if tweet[-1] == '':
		pass
	else:	
		cur.execute(statement_2, tweet)
conn.commit()




statement_3 = 'INSERT OR IGNORE INTO Users Values (?,?,?,?,?,?,?)'

for user in List_of_tweet_user_tuples:
	cur.execute(statement_3, user)
		
conn.commit()







# *************Join statments ************************************


# Statment 1 will be an INNER Join matching movie title in MOVIES and favorites and user_id TWeets to see which tweet that mentioned a movie was favorited the most and the user_id of that person

# Statement 2 will Join getMovieAudience, Plot, Actors, and Imdb_rating to return important information about the Movie

# Statement 3 will be an InnerJoin selecting Tweets favorites with Movies titles and year to see  if tweets about more recent movies get more favorites
Intresting_movie_data = 'SELECT Title, plot, Rated, Audience, Rating FROM Movies'
cur.execute(Intresting_movie_data)
cool_movie_data = cur.fetchall()
# print (str(cool_movie_data))


Director_movies_tweeted = 'SELECT Movies.Title, Tweets.search_term, Tweets.movie_id FROM Movies INNER JOIN Tweets ON Movies.Director = Tweets.search_term'
cur.execute(Director_movies_tweeted)
Dir_data = cur.fetchall()
# print (Dir_data)

Publicity_tweeters = 'SELECT Tweets.search_term, Users.num_followers, Users.screen_name FROM Tweets INNER JOIN Users on Tweets.user_id = Users.user_id'
cur.execute(Publicity_tweeters)
public_data = cur.fetchall()
# print (public_data)
#************************* DATA PROCESSING**************************************

conn.close()

# DATA processing 1 and 2: Mapping and Collections

def get_publicity_tweeters(object):
	return (object[0], object[1])

diction_listvals = collections.defaultdict(list)

tweeters = map(get_publicity_tweeters,public_data)
counter = 0
for a,b in tweeters:
	diction_listvals[a].append(b)
	new_followers_list = diction_listvals	
	# print(new_followers_list)
for x in new_followers_list:
	print (x)
	for values in new_followers_list[x]:
		# print (values)
		counter += values
	new_followers_list[x] = counter		
	print (new_followers_list)

outputlist_1 = []

a = list(new_followers_list.items())
# print (a)
for tuples in a:
	b = list(tuples)
	string = 'The total number of followers from users and users mentioned in tweets about Director ' + str(b[0]) +' is ' +str(b[1]) + '\n\n'
	outputlist_1.append(string)
	




# Data Processing 3: Dictionary Accumulation

James_Cameron_dict = {'Avatar':0, 'tweets about another movie':0}
Ridley_Scott_dict = {'Gladiator':0, 'tweets about another movie':0}
David_Anspaugh_dict = {'Hoosiers':0, 'tweets about another movie':0}
for tuples in Dir_data:
	if tuples[1] == 'James Cameron':
		if tuples[2] != '':
			if tuples[0] not in James_Cameron_dict:
				James_Cameron_dict[tuples[0]] = 1
			else:
				James_Cameron_dict[tuples[0]] += 1
		else:
			if 'tweets about another movie' not in James_Cameron_dict:
				James_Cameron_dict['tweets about another movie'] = 1
			else:
				James_Cameron_dict['tweets about another movie'] += 1
	elif tuples[1] == 'Ridley Scott':
		if tuples[2] != '':
			if tuples[0] not in Ridley_Scott_dict:
				Ridley_Scott_dict[tuples[0]] = 1
			else:
				Ridley_Scott_dict[tuples[0]] += 1
		else:
			if 'tweets about another movie' not in Ridley_Scott_dict:
				Ridley_Scott_dict['tweets about another movie'] = 1
			else:
				Ridley_Scott_dict['tweets about another movie'] += 1
	if tuples[1] == 'David Anspaugh':
		if tuples[2] != '':
			if tuples[0] not in David_Anspaugh_dict:
				David_Anspaugh_dict[tuples[0]] = 1
			else:
				David_Anspaugh_dict[tuples[0]] += 1
		else:
			if 'tweets about another movie' not in David_Anspaugh_dict:
				David_Anspaugh_dict['tweets about another movie'] = 1
			else:
				David_Anspaugh_dict['tweets about another movie'] += 1						
List_director_dicts = []
List_director_dicts.append(James_Cameron_dict)		
List_director_dicts.append(Ridley_Scott_dict)
List_director_dicts.append(David_Anspaugh_dict)			

List_of_output_strings_2 = []
for director in List_director_dicts:
	if "Avatar" in director:
		Output_1 = 'Out of all the tweets searched about James Cameron ' + str(director['Avatar']) + ' were about Avatar and ' + str(director['tweets about another movie']) + ' tweets were about another movie' + '\n\n'
		List_of_output_strings_2.append(Output_1)
	if 'Gladiator' in director:
		Output_2 = 'Out of all the tweets searched about Ridley Scott ' + str(director['Gladiator']) + ' were about Gladiator and ' + str(director['tweets about another movie']) + ' tweets were about another movie' + '\n\n'
		List_of_output_strings_2.append(Output_2)
	if 'Hoosiers' in director:
		Output_3 = 'Out of all the tweets searched about David Anspaugh ' + str(director['Hoosiers']) + ' were about Hoosiers and ' + str(director['tweets about another movie']) + ' tweets were about another movie' + '\n\n'
		List_of_output_strings_2.append(Output_3)	



# Data Processing 4: 

output_string_list_3 = []
rating_output = sorted(cool_movie_data, key = lambda x: x[-2], reverse = True)
for a in rating_output:
	output_string_3 = 'The movies are sorted by rating. A cool thing about ' + str(a[0]) + ' is that ' + str(a[3]) + ' and it is rated ' + str(a[2]) + '. The plot of this movie is ' + str(a[1])  + ' Lastly ' + str(a[4]) + '\n\n'
	output_string_list_3.append(output_string_3)
	

#******** Write to a Text File *******************************




# Write my output from the 4 data manipulations into  test file

final_file = 'Finalproject_206.txt'
opened_file = open(final_file,'w')
opened_file.write('The three movies are Avatar, Hoosiers and Gladiator. The directors of the movies are James Cameron, David Anspaugh and Ridley Scott. The date is 4/25/17 \n\n')
for a in outputlist_1:
	opened_file.write(a + '\n\n')
for b in List_of_output_strings_2:
	opened_file.write(b)	
for c in output_string_list_3:
	opened_file.write(c)
opened_file.close()	


# a = ('10',football,tennis)
# b = get_publicity_tweeters(a)
# print (type(b))
# print (b)

# ********************* TEST CASES *******************************
# Put your tests here, with any edits you now need from when you turned them in with your project plan.

# Attempt is an "instance of a movie"

class Classes_Tests(unittest.TestCase):
	
	def test_1(self):
		attempt = list_of_movie_instances[0]
		self.assertEqual(type(attempt.movieAppeal()), type('a'), "testing type of return value of movieAppeal method in the Movie Class")
	def test_2(self):
		attempt = list_of_movie_instances[0]
		self.assertEqual(attempt.num_of_languages(), 1, 'Testing the return value of num_of_langauges method')	
	def test_3(self):
		attempt = list_of_movie_instances[0]
		self.assertEqual(attempt.title, movie_1, 'Testing side effect of the consturctor to see if the instance variable is correct')
	def test_4(self):
		attempt = list_of_movie_instances[0]
		self.assertEqual(attempt.imdb_rating, 8.5, 'Testing the side effect of the constructor to see if if the instance variable self.imdb_rating returns the correct rating')
	def test_5(self):
		attempt = list_of_movie_instances[0]
		self.assertEqual(attempt.getMovieAudience(), 'The Critics like it more', 'Testing the return value of the getMovideAudience method')
	def test_6(self):
		self.assertEqual(len(list_of_movie_instances), 3, 'Testing that the list of Movie instances has 3 or more instances of a movie') 
	def test_7(self):
		attempt = List_of_tweet_instances[0]
		b =attempt.search_term
		self.assertIn(b, List_twitter_search_Directors, 'Testing that the search term for this instance is one of the directors from our searched movies')
	def test_8(self):
		attempt = List_of_tweet_instances[0]
		self.assertIsInstance(attempt,Tweet, 'Checking to see if this is an instance of the Class Tweet')
	def test_9(self):
		attempt = List_of_tweet_User_instances[0]
		self.assertIsInstance(attempt,TweetUser, 'Checking to see if this is an instance of the Class TweetUser')
	def test_10(self):
		attempt = list_of_movie_instances[0]
		self.assertIsInstance(attempt, Movie, 'Checking to see if this is an instance of the Class Movie')				




class Caching_Tests(unittest.TestCase):
	def test_1(self):
		file = 'SI206_final_project_cache.json'
		test_string = open(file, 'r')
		reading_string = test_string.read()
		self.assertTrue('Avatar' in reading_string, 'Checking to see if Avatar is in the movie cache file')
		test_string.close()
	def test_2(self):
		file = 'SI206_final_project_cache.json'
		test_string = open(file, 'r')
		reading_string = test_string.read()
		self.assertTrue('Hoosiers' in reading_string, 'Checking to see if Hoosiers is in the movie cache file')
		test_string.close()	
	def test_3(self):
		a = getwithcaching('The Dark Knight')
		self.assertEqual(type(a),type({}),'Checking to make sure getwithcaching returns the correct type')
	def test_4(self):
		a = get_tweetdata_with_caching('Steven Spielberg')
		self.assertEqual(type(a),type([]),'Checking to make sure get_tweetdata_with_caching returns the correct type')
	def test_5(self):
		a = get_user_tweets_information('TropicalEilend')
		self.assertEqual(type(a),type({}),'Checking to make sure get_user_tweets_information returns the correct type')			




class Database_Tests(unittest.TestCase):
	
	def test_1(self):
		conn = sqlite3.connect('Final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==7,"Testing that there are 7 columns in the Users database")
		conn.close()

	def test_2(self):
		conn = sqlite3.connect('Final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[2])==11,"Testing that there are 9 columns in the Movies table")
		conn.close()	
	def test_3(self):
		conn = sqlite3.connect('Final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==7,"Testing that there are 7 columns in the Users database")
		conn.close()
	def test_4(self):
		conn = sqlite3.connect('Final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=10,"Testing that there are at least 10 distinct users in the Users table")		
	def test_5(self):
		conn = sqlite3.connect('Final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result)>=3, "Testing there are at least 3 Movies being loaded into the Movies datab")



class ProcessTest(unittest.TestCase):
	def test_1(self):
		test_tuple = ('baseball','football','tennis')
		Test_function = get_publicity_tweeters(test_tuple)
		self.assertEqual(type(Test_function), type(()), 'Checking if this function has the right output')
	def test_2(self):
		test_tuple = ('baseball','football','tennis')
		Test_function = get_publicity_tweeters(test_tuple)
		self.assertEqual(Test_function, ('baseball','football'), 'Checking if this function has the right output')					
## Remember to invoke all your tests...

unittest.main(verbosity=2) 