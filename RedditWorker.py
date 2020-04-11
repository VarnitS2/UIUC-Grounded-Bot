import praw

redditClientSecretFileName = "reddit_client_secret.txt"

def initializeRedditInstance():
    with open(redditClientSecretFileName) as f:
        tokens = f.readline().split(", ")
        reddit = praw.Reddit(client_id=tokens[0], client_secret=tokens[1], user_agent=tokens[2])
        return reddit

def getRandomMeme():
    print('Running')

if __name__ == '__main__':
    reddit = initializeRedditInstance()
    subreddit = reddit.subreddit('memes')
