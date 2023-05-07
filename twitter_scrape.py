import pandas as pd
import pymongo
import streamlit as st
import time
import datetime
import snscrape.modules.twitter as sntwit

# Creating connection to No sql database
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["twitter_data"]
tweets_df = pd.DataFrame()
mini_df = pd.DataFrame()

# Creating Streamlit dash board ---------1
st.title('Twitter Data Scrapper')
choices = st.selectbox("What you are looking for?", ['Keyword', 'Hashtag'])
inputt = st.text_input(
    "Enter keyword that you want to search", 'Example: Bit Coin Market')
start_date = st.date_input("Enter the Start date",
                           datetime.date(2000, 1, 1), key='1')
end_date = st.date_input("Enter the End date",
                         datetime.date(2023, 1, 1), key='2')
tweet_count = st.number_input("No. of tweets to scrape?", 0, 1000, 5)

# Scraping data using snscrape
tweets = []
if inputt:
    try:
        if choices == 'Keyword':
            for a, twt in enumerate(sntwit.TwitterSearchScraper(f'{inputt} since:{start_date} until:{end_date}').get_items()):
                if a > tweet_count:
                    break
                tweets.append([twt.date, twt.id, twt.user.username, twt.content, twt.lang,
                              twt.likeCount, twt.replyCount, twt.retweetCount, twt.source, twt.url])
            tweets_df = pd.DataFrame(tweets, columns=[
                                     "Date", "ID", "User", "Content", "Language", "Like Count", "Reply Count", "Retweet Count", "Source", "URL", ])
        else:
            for a, twt in enumerate(sntwit.TwitterHashtagScraper(f'{inputt} since:{start_date} until:{end_date}').get_items()):
                if a > tweet_count:
                    break
                tweets.append([ twt.date, twt.id, twt.user.username, twt.content, twt.lang, twt.likeCount, twt.replyCount,twt.retweetCount, twt.source, twt.url ])
            tweets_df=pd.DataFrame(tweets,columns=["Date", "ID", "User","Content","Language","Like Count", "Reply Count", "Retweet Count", "Source", "URL", ])
    except Exception as e :
        st.error('Apologies for Inconvenience Cause, Please try again Later')
else:
  st.warnings("Kindly make a Choice")

@st.cache # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):    
    return df.to_csv().encode('utf-8')
    
if not tweets_df.empty:
    st.download_button('Download CSV', tweets_df.to_csv(), file_name='twitter_scrape.csv', mime="text/csv")        
    st.download_button('Download JSON', tweets_df.to_json(), file_name='twitter_scrape.json', mime="text/json")
    if st.button('Upload Tweets to Database'):
        mycollection=mydb[inputt.replace(' ','_')+'_Tweets']
        dict=tweets_df.to_dict('records')
        if dict:
            mycollection.insert_many(dict) 
            timestmp = time.time()
            mycollection.update_many({}, {"$set": {"KeyWord_or_Hashtag": inputt+str(timestmp)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database')
            st.balloons()
        else:
            st.warning('Data Can\'t be uploaded as there is no tweets')

    if st.button('Show Tweets df'):
        st.write(tweets_df)

# SIDEBAR
with st.sidebar:   
    st.write('Datasets: ')
    for l in mydb.list_collection_names():
        my_collection=mydb[l]       
        if st.button(l):            
            mini_df = pd.DataFrame(my_collection.find({}, projection={ "_id": 0 }))

# DISPLAY THE DOCUMENTS IN THE SELECTED COLLECTION
if not mini_df.empty: 
    st.write(f'({len(mini_df)} Records Found')
    st.write(mini_df) 
