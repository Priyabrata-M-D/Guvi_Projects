import snscrape.modules.twitter as sntwitter
import pandas as pd


# Define a function to scrape Twitter data
def scrape_twitter_data(hashtag, start_date, end_date, max_tweets):
    tweets_list = []
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(f'{hashtag} since:{start_date} until:{end_date}').get_items()):
        if i >= max_tweets:
            break
        tweets_list.append(
            [tweet.date, tweet.id, tweet.url, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.lang, tweet.source, tweet.likeCount])
    tweets_df = pd.DataFrame(tweets_list,
                             columns=["Date", "ID", "URL", "User", "Reply Count", "Retweet Count",
                                      "Language",
                                      "Source", "Like Count"])
    return tweets_df
