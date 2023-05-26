import time
import tweepy
import re
import sys

all_keys = open("keys.txt", "r").read().split("\n")

exception_object = {
    "si" : "is",
    "no" : "on",
    "pau" : "uap",
    "bernat" : "natber",
    "jordi" : "dijor",
    "nico" : "coni",
    "marc" : "rcma",
    "gerard" : "rar",
    "nacho" : "chona",
    "miner" : "nermi",
    "tontito" : "titon",
    "tontita" : "titon",
    "perdo" : "doper",
}

def authenticate():
    api_key = all_keys[0]
    api_secret_key = all_keys[1]
    access_token = all_keys[2]
    access_token_secret = all_keys[3]

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit = True)
    print('Auth successful.')
    # Get info about the authenticated user
    user_id = api.verify_credentials().id_str
    
    return api, user_id

def tweet(api, tweet):
    api.update_status(tweet)
    print("Tweeted: {}".format(tweet))


def estrematize(word):

    if word in exception_object:
        return exception_object[word]
    else:
        # Si nomes es una lletra, retornem
        if len(word) == 1 or len(word) == 2:
            return word

        # Si es mes de una lletra, estrematitzem la paraula
        vocals = "aeiou"
        diftongs = ["ai", "ei", "oi", "ui", "au", "eu", "iu", "ou", "ia", "ie", "io", "iu", "ua", "ue", "ui", "uo"]
        silabes = []
        silaba = ""
        prev_letter = ""
        for letter in word:
            silaba += letter
            if letter in vocals:
                if prev_letter+letter not in diftongs:
                    silabes.append(silaba)
                    silaba = ""
            prev_letter = letter

        if silaba:  # si hi ha una última sil·laba sense vocal, l'afegim
            silabes.append(silaba)

        if len(silabes) == 1:
            return silabes[0]  # si només hi ha una sil·laba, la retornem
        else:
            return silabes[-1] + ''.join(silabes[:-1])  # si hi ha més d'una, posem l'última al davant i unim les altres

    
def normalize (word):
    word = word.lower()
    weird_letters = ["à", "è", "é", "í", "ó", "ò", "ú", "ü"]
    normal_letters = ["a", "e", "e", "i", "o", "o", "u", "u"]
    for i in range(len(weird_letters)):
        word = word.replace(weird_letters[i], normal_letters[i])
    return word

def formatTweet (text):
    tweet_text = mention.text.split(" ")
    if '@estrematic' in tweet_text:
        tweet_text.remove("@estrematic")
    estrematized_tweet = ""
    for word in tweet_text:
        question = False
        exclamation = False
        if '?' in word:
            question = True
            word.replace("?", "")
        if '!' in word:
            word.replace("!", "")
            exclamation = True
        if '.' in word:
            word.replace(".", "")
        if ',' in word:
            word.replace(",", "")
        estrematized_tweet += estrematize(normalize(word)) 
        if question:
            estrematized_tweet += "?"
        if exclamation:
            estrematized_tweet += "!"
        estrematized_tweet += " "
    
    if question:
        estrematized_tweet += "?"
    if exclamation:
                    estrematized_tweet += "!"

# The goal of this application is to reply to every mention with the estrematized version of the word.
# If we have already replied to a mention, we don't reply again.
# We also don't reply to our own tweets.
if __name__ == "__main__":
    # If the first argument is "debug", we don't tweet, we just print the estrematized tweet
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        print("debug mode")
    else:
        while True:
            api, user_id = authenticate()
            mention_id = 1
            mentions_file = open("mentions.txt", "a")
            for mention in api.mentions_timeline():
                have_we_replied = mention.id_str in open("mentions.txt", "r").read().split("\n")
                mentions_file.close()
                # When working, change == to !=
                if mention.in_reply_to_status_id is None and mention.user.id_str != user_id and not have_we_replied:
                    print("replying to tweet: {}".format(mention.text))
                    mentions_file = open("mentions.txt", "a")
                    mentions_file.write(mention.id_str + "\n")
                    mentions_file.close()
                    
                    estrematized_tweet = formatTweet(mention.text)
                    print("Estrematized tweet: {}".format(estrematized_tweet))
                    #try:
                    #    api.update_status(status=estrematized_tweet, in_reply_to_status_id=mention.id_str, auto_populate_reply_metadata=True)
                    #except tweepy.TweepError as e:
                    #    print(e)               
            time.sleep(15)

    


        
