import praw
import os
import re
import random
import pdb

def getReponse():
    randIndex = random.randint(0, (len(responses) - 1))
    return responses[randIndex]

def searchForKeyword(scope):
    return re.search("!magicball", scope, re.IGNORECASE)

def replyToChildren(comment):
    for child in comment.replies:
        if re.search("!magicball", child.body, re.IGNORECASE):
            if child.id not in completed_comments:
                child.reply(getReponse())
                completed_comments.append(child.id)
                print("Replied")
        else:
            replyToChildren(child)

reddit = praw.Reddit("bot2")
subreddit = reddit.subreddit("snifferdog2")

responses = []
with open("responses.txt", "r") as f:
    lines = list(filter(None, f.read().split("\n")))
    for i in lines:
        responses.append(i)
print("Valid Responses: ", responses)

if not os.path.isfile("completed_comments.txt"):
    completed_comments = []
else:
    with open("completed_comments.txt", "r") as f:
        completed_comments = list(filter(None, f.read().split("\n")))

for submission in subreddit.new(limit=5):
    for comment in submission.comments:
        if searchForKeyword(comment.body):
            if comment.id not in completed_comments:
                comment.reply(getReponse())
                completed_comments.append(comment.id)
        replyToChildren(comment)
    with open("completed_comments.txt" , "w") as f:
        for i in completed_comments:
            f.write(i + "\n")
