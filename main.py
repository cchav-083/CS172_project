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

    
    feeds.append(json.dumps(dict))
    with open("sample.json", "w") as f:



    #feeds.append(dict)
    print("feed: ", feeds)

   # with open("sample.json", mode='w') as f:
    #    f.write(json.dumps(feeds, indent=2))

    pass

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



reddit = praw.Reddit(
    client_id="URr1kFlz0I14JXM5fWzxdA",
    client_secret="Ie89Czek_-6enr0KekkLcI_KUEmtCQ",
    user_agent = "cs172 crawler"
)

subreddit = reddit.subreddit("python")

top_posts = subreddit.top(limit=2)
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
dicts = []
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

    print(post_dat)
    dicts.append(post_dat)
   # dict_to_json(post_dat)
    #feed_json(post_dat)
    #feed_json(post_dat)

dict_to_json(dicts)


#def main():
#    pass

