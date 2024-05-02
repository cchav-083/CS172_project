import praw

reddit = praw.Reddit(
    client_id="URr1kFlz0I14JXM5fWzxdA",
    client_secret="Ie89Czek_-6enr0KekkLcI_KUEmtCQ",
    user_agent = "cs172 crawler"
)

subreddit = reddit.subreddit("python")

top_posts = subreddit.top(limit=10)
new_posts = subreddit.new(limit=10)

for post in top_posts:
    print("Title - ", post.title)
    print("ID - ", post.id)
    print("Author - ", post.author)
    print("URL - ", post.url)
    print("Score - ", post.score)
    print("Comment count - ",post.num_comments)
    print("Created - ", post.created_utc)
    print("\n")
    