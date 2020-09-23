import requests
import random


# This authenticates the bearer token
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


# GET request using bearer token returning 3200 of Elon's tweets
ElonResponse = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=elonmusk&count=3200',
                            auth=BearerAuth(
                                'AAAAAAAAAAAAAAAAAAAAAJWyHwEAAAAARwQLbI3LnE70KrXztCVAZuczBZU%3DhLtnzNoHtqFFbtJT7R0gMQs'
                                'iT91w15L9CuNCixfn1w6W6hnhaG'))
# GET request using bearer token for returning 3200 of Kanye's tweets
KanyeResponse = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=kanyewest&count=3200',
                             auth=BearerAuth(
                                 'AAAAAAAAAAAAAAAAAAAAAJWyHwEAAAAARwQLbI3LnE70KrXztCVAZuczBZU%3DhLtnzNoHtqFFbtJT7R0gMQ'
                                 'siT91w15L9CuNCixfn1w6W6hnhaG'))

# Change to json body
ElonResponse = ElonResponse.json()
KanyeResponse = KanyeResponse.json()


# Filters tweets considered not genuine to Elon and Kanye (retweets, replies, tags, references, links, etc)
def filtering_tweets(response):
    tempArray = []
    for i in range(len(response)):
        if '@' not in response[i]['text'] and 'https' not in response[i]['text']:
            tempArray.append(response[i]['text'])  # this array only includes tweets genuine to Elon and Kanye
    return tempArray


# Filtering tweets for both Elon's tweets and Kanye's tweets
filteredElonTweets = filtering_tweets(ElonResponse)
filteredKanyeTweets = filtering_tweets(KanyeResponse)

numberCorrect = 0  # number of tweets guessed correctly
totalTweetsPrompted = 0  # total number of tweets prompted to user


# gets random tweet
def random_line():
    global arrayIndex  # index to randomly choose from either Elon or Kanye's tweets
    global tweetIndex  # index to randomly choose a single tweet from array of Elon/Kanye tweets
    if arrayIndex == 1:  # 1 means Elon
        tweetIndex = random.randrange(0, len(filteredElonTweets))
        return filteredElonTweets[tweetIndex]
    else:  # 0 means Kanye
        tweetIndex = random.randrange(0, len(filteredKanyeTweets))
        return filteredKanyeTweets[tweetIndex]


# prompts user to guess tweet and displays if correct/incorrect
def prompt_user():
    global arrayIndex  # index to randomly choose from either Elon or Kanye's tweets
    global numberCorrect  # number of tweets guessed correctly
    global totalTweetsPrompted  # total number of tweets prompted to user
    global tweetIndex  # index to randomly choose a single tweet from array of Elon/Kanye tweets

    print("Kanye tweets remaining: " + str(len(filteredKanyeTweets)))
    print("Elon tweets remaining: " + str(len(filteredElonTweets)))

    # prompt user and get user input
    print("Is the following tweet Elon or Kanye's tweet?" + "\n" + randomTweet)
    userInput = raw_input("Your Answer: ")  # using python 2.7 so used raw_input instead of input

    # print if guess was correct/incorrect
    if userInput.lower() == "elon" and arrayIndex == 1:
        print("You are correct, this is Elon's tweet.")
        numberCorrect += 1
    elif userInput.lower() == "kanye" and arrayIndex == 0:
        print("You are correct, this is Kanye's tweet.")
        numberCorrect += 1
    else:
        print("You are incorrect.")

    # remove tweet from array of tweets
    if arrayIndex == 1:  # 1 is elon
        filteredElonTweets.pop(tweetIndex)
    else:  # 0 is kanye
        filteredKanyeTweets.pop(tweetIndex)

    totalTweetsPrompted += 1


# My game stops when either all of Kanye's tweets OR all of Elon's tweets have been prompted.
while len(filteredKanyeTweets) > 0 and len(filteredElonTweets) > 0:
    arrayIndex = random.randrange(0, 2)  # index to randomly choose from either Elon or Kanye's tweets
    tweetIndex = 0  # index to randomly choose a single tweet from array of Elon/Kanye tweets
    randomTweet = random_line()  # gets random tweet
    prompt_user()  # prompts user to guess tweet and displays if correct/incorrect
    print  # blank line

# Game statistics displays after the game has ended
print("Game Statistics: ")
print("Total Number of Tweets Correct: " + str(numberCorrect))
print("Total Number of Tweets Prompted: " + str(totalTweetsPrompted))
percentage = (float(numberCorrect) / totalTweetsPrompted) * 100
print("Percentage Correct: " + str(percentage) + "%")
