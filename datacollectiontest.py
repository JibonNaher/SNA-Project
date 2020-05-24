import tweepy

import csv
import pandas as pd
import numpy as np
import time
from random import randint, random

# api_key <- "QbmMwUsdO2PmIePVQRRQJO45J"
#
# api_secret <- "GBxplPWkABq1VB5emsGDZXwHwyOfgnOS6bmPSmDbVlnjJUw3j2"
#
# access_token <- "1032491095790215168-TSDkviHjIK7CPIM8OE7uQaTvpqxmup"
#
# access_token_secret <- "RNXpNYI6AGs3lftUzK7fshlzAv6eIYMLhGoIb4CqFC9WI"

consumer_key = 'QbmMwUsdO2PmIePVQRRQJO45J'
consumer_secret = 'GBxplPWkABq1VB5emsGDZXwHwyOfgnOS6bmPSmDbVlnjJUw3j2'
access_token = '1032491095790215168-TSDkviHjIK7CPIM8OE7uQaTvpqxmup'
access_secret = 'RNXpNYI6AGs3lftUzK7fshlzAv6eIYMLhGoIb4CqFC9WI'
# tweetsPerQry = 10
# maxTweets = 10
# hashtag = "#ChiniseVirus"

authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def collectTweet():
	maxId = -1
	tweetCount = 0
	while tweetCount < maxTweets:
		if(maxId <= 0):
			newTweets = api.search(q=hashtag, count=tweetsPerQry, result_type="recent", tweet_mode="extended")
		else:
			newTweets = api.search(q=hashtag, count=tweetsPerQry, max_id=str(maxId - 1), result_type="recent", tweet_mode="extended")

		if not newTweets:
			print("Tweet Habis")
			break

		for tweet in newTweets:
			print(tweet.created_at, ", text: ", tweet.full_text,  "retweet: ", tweet.retweet_count, " like count:", tweet.favorite_count, "\n")

		tweetCount += len(newTweets)
		maxId = newTweets[-1].id

def unique(initial_list):
	list_set = set(initial_list)
    # convert the set to the list
	unique_list = (list(list_set))
	return unique_list

def uniqueUserCount():
	userlist = []
	tweet_file = 'Data/tweets.csv'
	df = pd.read_csv(tweet_file)
	print("Total length of the file: ", len(df))
	for i in range(len(df)):
		tweet = df.iloc[i]
		if(pd.isnull(tweet.loc['reply_to_user_id'])):
			userlist.append(tweet.loc['screen_name'])
		else:
			#print(tweet.loc['reply_to_user_id'])
			continue
	print("user list length: ", len(userlist))
	userlist = unique(userlist)
	print("user list length after: ", len(userlist))

	with open("data/unique_user.csv","w") as f:
		wr = csv.writer(f,delimiter="\n")
		wr.writerow(userlist)
	return  userlist

def get_nonhatespeech_tweets(screen_name):
	#user_tweets = tweepy.Cursor(api.favorites, id=screen_name, lang = 'en', exclude_replies=True).items(10)
	#user_tweets = tweepy.Cursor(api.search, id=screen_name, result_type = 'popular', lang = 'en', exclude_replies=True).items(10)
	user_tweets = api.user_timeline(id=screen_name, count=10, lang = 'en', exclude_replies=True)
	# for tweet in user_tweets:
	# 	print("\n", tweet.id_str, tweet.created_at, tweet.text, tweet.retweet_count, tweet.favorite_count, "\n")

	# new_tweets = api.user_timeline(screen_name = screen_name,count=10, lang = 'en', exclude_replies=True)
	# #print(new_tweets)
	# for tweet in new_tweets:
	# 	print(tweet, "\n")

	outtweets = [[screen_name, tweet.id_str, tweet.created_at, tweet.text, tweet.retweet_count, tweet.favorite_count, tweet.in_reply_to_status_id_str, tweet.in_reply_to_screen_name, tweet.in_reply_to_user_id_str] for tweet in user_tweets]
	with open('data/users_tweets.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerows(outtweets)

def getUsers():
	userlist = []
	tweet_file = 'data/popular_tweets.csv'
	df = pd.read_csv(tweet_file)
	print("Total length of the file: ", len(df))
	for i in range(len(df)):
		tweet = df.iloc[i]
		userlist.append(tweet.loc['user_screen_name'])
	return userlist

# def getTweets():
# 	#popular_tweets = api.search(q='coronavirus OR #ChiniseVirus', result_type='popular', count=5)
# 	popular_tweets = api.search(q='#Chinavirus OR #WuhanVirus OR #ChinaLiedPeopleDied', result_type='popular', count = 18000, lang = "en", exclude_replies=True, include_rts = False)
# 	print(len(popular_tweets))
# 	# for tweet in  popular_tweets:
# 	# 	print(tweet.text, tweet.user.id, tweet.user.screen_name, tweet.user.location, tweet.user.followers_count, tweet.user.friends_count, tweet.user.listed_count, tweet.user.favourites_count, tweet.user.statuses_count)
# 	outtweets = [[tweet.id_str, tweet.user.id, tweet.user.screen_name, tweet.created_at, tweet.text, tweet.retweet_count, tweet.favorite_count, tweet.user.location, tweet.user.followers_count, tweet.user.friends_count, tweet.user.listed_count, tweet.user.favourites_count, tweet.user.statuses_count] for tweet in popular_tweets]
# 	with open('data/popular_tweets.csv', 'a') as f:
# 		writer = csv.writer(f)
# 		writer.writerows(outtweets)

	## id, screen_name, location, followers_count, friends_count, listed_count, favourites_count, statuses_count

def calc_median_favorites(user_id):
    fav_list = []
    tweets = api.user_timeline(id=user_id, count=100)

    for tweet in tweets:
        if tweet.text.startswith('RT'):
            continue
        else:
            fav_list.append(tweet.favorite_count)
    time.sleep(random() / 5)
    return np.median(fav_list)

def calc_median_retweets(user_id):
    rt_list = []
    tweets = api.user_timeline(id=user_id, count=100)

    for tweet in tweets:
        if tweet.text.startswith('RT'):
            continue
        else:
            rt_list.append(tweet.retweet_count)
    time.sleep(random() / 5)
    return np.median(rt_list)

def create_engagement_metric(df):
    working_df = df.copy()
    from sklearn.preprocessing import MinMaxScaler
    # Favorites
    fav_eng_array = df['median_favs'] / df['user_followers_count']
    scaler = MinMaxScaler().fit(fav_eng_array.values.reshape(-1, 1))
    scaled_favs = scaler.transform(fav_eng_array.values.reshape(-1, 1))

    # Retweets
    rt_eng_array = df['median_favs'] / df['user_followers_count']
    scaler = MinMaxScaler().fit(rt_eng_array.values.reshape(-1, 1))
    scaled_rts = scaler.transform(rt_eng_array.values.reshape(-1, 1))

    mean_eng = (scaled_favs + scaled_rts) / 2
    working_df['engagement'] = mean_eng
    return working_df

if __name__ == '__main__':
	# with open('data/popular_tweets.csv', 'w') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(["tweet_id", "user_id", "user_screen_name", "tweet_created_at","tweet_text", "tweet_retweet_count", "tweet_favorite_count", "user_location", "user_followers_count", "user_friends_count" , "user_listed_count", "user_favourites_count", "user_statuses_count"])
	#
	# getTweets()

	# userlist = uniqueUserCount()

	# userlist = getUsers()
	# print(userlist)
	# with open('data/users_tweets.csv', 'w') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(["screen_name", "tweet_id","created_at","text", "retweet_count", "favorite_count", "in_reply_to_status_id_str", "in_reply_to_screen_name", "in_reply_to_user_id_str" ])
	# for user in userlist:
	# 	print("current username: ", user)
	# 	get_nonhatespeech_tweets(user)
	# 	print("\n\n")

	tweet_file = 'data/popular_tweets.csv'
	df = pd.read_csv(tweet_file)
	df['median_favs'] = df['user_id'].apply(lambda x: calc_median_favorites(x))
	df['median_rts'] = df['user_id'].apply(lambda x: calc_median_retweets(x))
	df = create_engagement_metric(df)
	df = df.sort_values('engagement', ascending=False)
	df.to_csv('data/engagement_of_user_tweet.csv', index=False)



###### https://stackoverflow.com/questions/48589248/tweepy-extended-mode-with-api-search
# for self._tweet in tweepy.Cursor(self._api.search,q=self._screen_name,count=300, lang="en", tweet_mode="extended").items(300):
#     self._csvWriter.writerow([self._tweet.created_at, self._tweet.full_text.encode('utf-8')])
