import praw
import random
import urllib.request

redditClientSecretFileName = "reddit_client_secret.txt"
memeTempFileName = "Memes/temp.jpg"
random.seed()

def initializeRedditInstance():
    with open(redditClientSecretFileName) as f:
        tokens = f.readline().split(", ")
        reddit = praw.Reddit(client_id=tokens[0], client_secret=tokens[1], user_agent=tokens[2])
        return reddit

def getRandomMeme(reddit):
    subreddit = reddit.subreddit('memes')

    randomPost = random.randrange(0, 50)
    for count, post in enumerate(subreddit.top('week', limit=50)):
        if count == randomPost:
            urllib.request.urlretrieve(post.url, memeTempFileName)

    return memeTempFileName

if __name__ == '__main__':
    reddit = initializeRedditInstance()
    subreddit = reddit.subreddit('memes')
