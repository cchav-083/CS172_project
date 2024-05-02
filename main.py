import praw
import json
import math
import os


def dict_to_json(dict):

    #print(dict)

    with open("sample.json", "w") as json_file: 
        
        json.dump(dict, json_file)


reddit = praw.Reddit(
    client_id="URr1kFlz0I14JXM5fWzxdA",
    client_secret="Ie89Czek_-6enr0KekkLcI_KUEmtCQ",
    user_agent = "cs172 crawler"
)

subreddit = reddit.subreddit("python")

top_posts = subreddit.top(limit=1)
new_posts = subreddit.new(limit=10)

post_data = {
    "title": None,
    "body":[
        {"content":None,
         "urls":[],
         "imgs":[]
        }
    ],
    "op":None,
    "id":None,
    "upvotes":None,
    "downvotes":None,
    "url":None,
    "comments": [
        {
            "username":None,
            "comment":None
        }
    ]


}

for post in top_posts:
    post_dat = {}
    #print("Title - ", post.title)
    post_dat["title"] = post.title

   # print("ID - ", post.id)
    post_dat["ID"] = post.id



   # print("Author - ", post.author)
    post_dat["author"] = post.author.name

   # print("URL - ", post.url)
    post_dat['url'] = post.url

   # print("Score - ", post.score)
    post_dat['score'] = post.score

   # print("Comment count - ",post.num_comments)
    post_dat["num_comments"] = post.num_comments

    #print("Created - ", post.created_utc)
    post_dat["post_created"] = post.created_utc


    #post_dat["body"] = print(post.selftext)

    #print("\n")

    #print(post_dat)

    #if not os.path.isfile("test.json"):
    #    print('exists')

    sample_dict = {
        "title":"hi world"
    }
    print(post_dat)
    dict_to_json(post_dat)



