import praw
import json
import math
import os

#feed one dictionary
#DOESNT work yet, ignore
def feed_json(dict):
    #json exists
    with open("sample.json", "r") as feedsjson:
        feeds = json.load(feedsjson)

    print(feeds)


    #feeds.append(json.dumps(dict))
    #with open("sample.json", "w") as f:
    #    pass


    #feeds.append(dict)
   # with open("sample.json", mode='w') as f:
    #    f.write(json.dumps(feeds, indent=2))


#needs an array of dictionaries
def dict_to_json(dicts):
    full_text = ""

    #print(dict)
    with open("sample.json", "w") as json_file: 
        
        json_file.write('[')
        for dict in dicts:
            text = json.dumps(dict)
            text+= ',\n'
            full_text+=text
            

        full_text =  full_text[:-2]
        json_file.write(full_text)


        json_file.write(']')


#returns array of dictionaries
def extract_posts(posts):
    dicts = []
    for post in posts:
        if post.over_18:
            print('over 18, skipping')
            continue

        post_dat = {}

        post_dat["title"] = post.title
        post_dat["ID"] = post.id

        if post.author is not None:
            post_dat["author"] = post.author.name
        else:
            post_dat["author"] = "deleted"

        post_dat['url'] = post.url

        post_dat['score'] = post.score
        post_dat['ratio'] = post.upvote_ratio
        post_dat["num_comments"] = post.num_comments
        post_dat["post_created"] = post.created_utc

        post_dat["comments"] = []

        post.comments.replace_more(limit=None)
        for top_level_comment in post.comments.list():
            post_dat["comments"].append(top_level_comment.body)
            #print(top_level_comment.body)

        post_dat["body"] = post.selftext
  
        dicts.append(post_dat)

    return dicts





def main(): 

    reddit = praw.Reddit(
        client_id="URr1kFlz0I14JXM5fWzxdA",
        client_secret="Ie89Czek_-6enr0KekkLcI_KUEmtCQ",
        user_agent = "cs172 crawler"
    )

    #GOAL : get 100,000 posts.
    subreddits = ["python"]

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)

        top_posts = subreddit.top(limit=1000)
        new_posts = subreddit.new(limit=1000)

    
        posts = extract_posts(top_posts)
        posts+= extract_posts(new_posts)
        dict_to_json(posts)
    

  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main()