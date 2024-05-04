import praw
import json
import math
import os
import userinfo
import time

import requests
from bs4 import BeautifulSoup
import re
import prawcore

from requests.exceptions import ConnectionError

#byte_counter = 0
#file_count = 0
#Looks for external links under reddit posts. 
#Returns a list of strings : urls
def crawl_urls(text : str):

    urls = re.findall("(?P<url>https?://[^\s]+)", text)
    return urls
    pass

#Uses the list of urls and requests them. Grabs their HTML and turns into a dictionary.
#do this for all urls in the list
#returns a list of dictionaries 
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
            if soup.title is not None:
                ext_link["title"] = soup.title.string

            if soup.get_text() is not None: 
                ext_link["description"] = soup.get_text() #useful for part b? 
            ext_link["url"] = url

            external_links.append(ext_link)


        except ConnectionError as e:
            req = "no response"
        
    return external_links
       

####
#ignore this, i never use this function.
###
def feed_json(dict, subreddit_name):
    #json exists
    feeds = None
    with open(("/data/"+subreddit_name+ ".json"), "r") as feedsjson:
        feeds = json.load(feedsjson)

    print(feeds)

    feeds = feeds[:-1]
    text = json.dumps(dict)
    feeds+=text
    feeds = feeds[:-2]
    feeds+= ']'

    filename = subreddit_name + '.json'
    if not os.path.exists('data'):
        os.makedirs('data')
        print('hello')

    with open(os.path.join('data', filename), "w") as json_file:
        json_file.write(feeds)

#needs an array of dictionaries
def create_json(dicts, subreddit_name):
    full_text = ""

    #print(dict)
    filename = subreddit_name + '.json'
    
    with open(os.path.join('data', filename), "w") as json_file:
        
        json_file.write('[')
        for dict in dicts:
            text = json.dumps(dict)
            text+= ',\n'
            full_text+=text
            

        full_text =  full_text[:-2]
        json_file.write(full_text)


        json_file.write(']')


#returns array of dictionaries
def extract_posts(posts, sub):
    dicts = []
    post_counter = 0
    for post in posts:
        
        counter = 0
        if post.over_18:
            print('over 18, skipping')
            continue
        while (counter < 100):
            try:
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
                post_dat["subreddit"] = sub
                        

                post_dat["body"] = post.selftext

                urls = crawl_urls(post.selftext)
                #print('crawling done')

                post_dat["external_links"] = scrape_urls(urls)

                #print('soup made')

                post_dat["comments"] = []

                        
                #FOR COMMENTS
                print('starting comments..')
                post.comments.replace_more(limit=None)
                #print('starting loop')
                print('comments recieved...')
                for top_level_comment in post.comments.list():
                    post_dat["comments"].append(top_level_comment.body)
                print('comments collected')
                
                dicts.append(post_dat)
                counter+=100 #this is so that the while loop breaks.
                post_counter+=1


                #check byte_count. if over 10million, create_json(dicts), and reset.

                    #time.sleep(1)
            except prawcore.exceptions.TooManyRequests as e:
                time.sleep(60)
                counter+=1
                print('too many requests! waiting 60 seconds..')
        
        print(post_counter)
        #time.sleep(1)
    return dicts





def main(): 

        #change this!!
    #subreddits = ["pics", "AskReddit"]
    subreddits = ['NintendoSwitch', 'mario', 'zelda', 'truezelda', 'patientgamers']

    print("starting")
    print(userinfo.useragent)

    
    reddit = praw.Reddit(
        client_id="URr1kFlz0I14JXM5fWzxdA",
        client_secret="Ie89Czek_-6enr0KekkLcI_KUEmtCQ",
        user_agent = userinfo.useragent
    )

    


    for sub in subreddits:
        print('crawling ', sub)
        subreddit = reddit.subreddit(sub)


        top_posts = subreddit.top(limit=1000)
        new_posts = subreddit.new(limit=1000)
        hot_posts = subreddit.hot(limit=1000)
       # contro_posts = subreddit.controversial(limit=1)

        posts = []
        posts +=extract_posts(hot_posts, sub)
        posts += extract_posts(top_posts, sub)
        posts+= extract_posts(new_posts, sub)
        

        create_json(posts, sub)

        
       # create_json(posts, sub)
   
    

  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main()