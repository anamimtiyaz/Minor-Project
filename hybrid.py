import string
from collections import Counter

import matplotlib.pyplot as plt
import sys
# from utils import process_tweet
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import time
start_time = time.time()




#
# nltk.download('all')
# text = open('read.txt', encoding='utf-8').read()
# lower_case = text.lower()
# cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
#




# Bech m se liya hua data


def get_tweets():
    import GetOldTweets3 as got
    twt = ''
    if(len(sys.argv) == 1): twt = 'CoronaOutbreak'
    else: twt = sys.argv[1]
    print('This plot is for - ' + twt)
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(twt) \
        .setSince("2002-11-01") \
        .setUntil("2020-06-01") \
        .setMaxTweets(1000)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    # Creating list of chosen tweet data
    text_tweets = [[tweet.text] for tweet in tweets]
    return text_tweets


# reading text file
text = ""
text_tweets = get_tweets()

length = len(text_tweets)

for i in range(0, length):
    text = text_tweets[i][0] + " " + text

# converting to lowercase
lower_case = text.lower()

# Removing punctuations
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))






# Using word_tokenize because it's faster than split()
tokenized_words = word_tokenize(cleaned_text, "english")

# Removing Stop Words
final_words = []
for word in tokenized_words:
    if word not in stopwords.words('english'):
        final_words.append(word)

# Lemmatization - From plural to single + Base form of a word (example better-> good)
# lemma_words = []
# for word in final_words:
#     word = WordNetLemmatizer().lemmatize(word)
#     lemma_words.append(word)
process_tweet(cleaned_text)

emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
        word, emotion = clear_line.split(':')

        if word in lemma_words:
            emotion_list.append(emotion)

print(emotion_list)
w = Counter(emotion_list)
print(w)


def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        print("Negative Sentiment")
    elif score['neg'] < score['pos']:
        print("Positive Sentiment")
    else:
        print("Neutral Sentiment")


sentiment_analyse(cleaned_text)

fig, ax1 = plt.subplots()
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()

print(time.time() - start_time)