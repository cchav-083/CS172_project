import praw
import json
import math
import os
import userinfo


import requests
from bs4 import BeautifulSoup
import re

from requests.exceptions import ConnectionError



#crawl 
def crawl_urls(text : str):

    urls = re.findall("(?P<url>https?://[^\s]+)", text)
    urls.append('https://op.Gg))')
    return urls
    pass
#V now send 
#returns a array of external links
#external_links = [ {"link": None, "title": None}]

def scrape_urls(urls : list):
    external_links = []
    for url in urls:
        #make a request
        
        url = url[:-1]
        print("url:" , url)

        try:
            req = requests.get(url)  

            html_doc = req.text

            soup = BeautifulSoup(html_doc, 'html.parser')


            ext_link = {}

            ext_link["title"] = soup.title.string
            ext_link["description"] = soup.get_text() #useful for part b? 
            ext_link["url"] = url

            external_links.append(ext_link)


        except ConnectionError as e:
            req = "no response"
        
    return external_links
       
#feed one dictionary
#DOESNT work yet, ignore
def feed_json(dict, subreddit_name):
    #json exists
    feeds = None
    with open((subreddit_name+ ".json"), "r") as feedsjson:
        feeds = json.load(feedsjson)

    print(feeds)

    feeds = feeds[:-1]
    text = json.dumps(dict)
    feeds+=text
    feeds = feeds[:-2]
    feeds+= ']'

    with open((subreddit_name+ ".json"), "w") as json_file:
        json_file.write(feeds)

#needs an array of dictionaries
def create_json(dicts, subreddit_name):
    full_text = ""

    #print(dict)
    with open(subreddit_name+".json", "w") as json_file: 
        
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
        post_dat['permalink'] = post.permalink

        post_dat['score'] = post.score
        post_dat['ratio'] = post.upvote_ratio
        post_dat["num_comments"] = post.num_comments
        post_dat["post_created"] = post.created_utc

        

        post_dat["body"] = post.selftext

        urls = crawl_urls(post.selftext)
        print('crawling done')

        post_dat["external_links"] = scrape_urls(urls)

        print('soup made')

        post_dat["comments"] = []
        post.comments.replace_more(limit=None)
        print('starting loop')
        for top_level_comment in post.comments.list():
            post_dat["comments"].append(top_level_comment.body)
            print(top_level_comment.body)


        print('done comments')
  
        dicts.append(post_dat)

    return dicts





def main(): 
    print("starting")
    print(userinfo.useragent)

    
    reddit = praw.Reddit(
        client_id="URr1kFlz0I14JXM5fWzxdA",
        client_secret="Ie89Czek_-6enr0KekkLcI_KUEmtCQ",
        user_agent = userinfo.useragent
    )
    #print(reddit.user_agent)
    #GOAL : get 100,000 posts.
    subreddits = ["python", "python"]
   # valo_id = "1ccwswy"
   # s_id = "1ccayuz"
    #subm = reddit.submission(id=valo_id)
    #print(subm.selftext)
    #print(subm.url)
    #print(subm.permalink)
   # scrape_urls(subm.selftext)


    #string_ex = "he one interested in the build &#x200B; [MeatRocket8#9272 - Summoner Stats - League of Legends (op.gg)](https://www.op.gg/summoners/euw/MeatRocket8-9272) &#&#x200B; here's my [op.Gg](https://op.Gg) for the one interested in the build &#x200B; [MeatRocket8#9272 - Summoner Stats - League of Legends (op.gg)](https://www.op.gg/summoners/euw/MeatRocket8-9272) &#x200B;"

    #urls = crawl_urls(string_)
   # urls = crawl_urls(subm.selftext)
    #scrape_urls(urls)
    #return

    for sub in subreddits:
        print('crawling ', sub)
        subreddit = reddit.subreddit(sub)


        top_posts = subreddit.top(limit=1)
        new_posts = subreddit.new(limit=1)
        hot_posts = subreddit.hot(limit=1)
        contro_posts = subreddit.controversial(limit=1)

        posts = []
        posts +=extract_posts(hot_posts)
        posts += extract_posts(top_posts)
        posts+= extract_posts(new_posts)
        

        create_json(posts, sub)

        
       # create_json(posts, sub)
    print('yes sir')
    

  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main()