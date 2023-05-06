import pandas as pd
import pymongo
import streamlit as st
import time, datetime
import snscrape.modules.twitter as sntwit

# Creating connection to No sql database
client=pymongo.MongoClient("mongodb://localhost:27017/")
mydb=client["twitter_data"]
tweets_df=pd.DataFrame()              

# Creating Streamlit dash board ---------1
st.title('Twitter Data Scrapper')
choices=st.selectbox("What you are looking for?", ['Keyword','Hashtag'])
input=st.text_input("Enter keyword that you want to search",'Example: Bit Coin Market')
start_date=st.date_input("Enter the Start date",datetime.date(2000,1,1),key='1')
end_date=st.date_input("Enter the End date",datetime.date(2023,1,1),key='2')
tweet_count=st.number_input("No. of tweets to scrape?", 0,1000,5)

#Scraping data using snscrape
tweets=[]
if input:
  try:
    if choices=='Keyword':
      for a,twt in enumerate(sntwit.TwitterSearchScraper(f'{input} since:{start_date} until:{end_date}').get_items()):
        if a>tweet_count:
          break
        tweets.append([ twt.date, twt.id, twt.user.username, twt.content, twt.lang, twt.likeCount, twt.replyCount,twt.retweetCount, twt.source, twt.url ])
      tweets_df=pd.DataFrame(tweets,columns=["Date", "ID", "User","Content","Language","Like Count", "Reply Count", "Retweet Count", "Source", "URL", ])
    else:
      for a,twt in enumerate(sntwit.TwitterHashtagScraper(f'{input} since:{start_date} until:{end_date}').get_items()):
        if a>tweet_count:
          break
        tweets.append([ twt.date, twt.id, twt.user.username, twt.content, twt.lang, twt.likeCount, twt.replyCount,twt.retweetCount, twt.source, twt.url ])
      tweets_df=pd.DataFrame(tweets,columns=["Date", "ID", "User","Content","Language","Like Count", "Reply Count", "Retweet Count", "Source", "URL", ])
  except Exception as e :
    st.error('Too many attempts, Try again later')
else:
  st.warnings("Kindly make a Choice")

with st.sidebar:   
    st.info('Info')
    if choices=='Keyword':
        st.info('Entered Keyword : '+input)
    else:
        st.info('Entered Hashtag : '+input)
    st.info('Start Date : '+str(start_date))
    st.info('End Date : '+str(end_date))
    st.info("Tweets Count : "+str(tweet_count))
    st.info("Tweets Scraped "+str(len(tweets_df)))
    disp=st.button('Show Tweets',key=1)

@st.cache # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):    
    return df.to_csv().encode('utf-8')
    
if not tweets_df.empty:
    z1, z2, z3=st.columns(3)
    with z1:
        csv=st.download_button('Download CSV', tweets_df.to_csv(), file_name='twitter_scrape.csv', mime="text/csv")        
    with z2:
        json=st.download_button('Download JSON', tweets_df.to_json(), file_name='twitter_scrape.json', mime="text/json")

    with z3:
        disp1=st.button('Show Tweets',key=2)
    if st.button('Upload Tweets to Database'):
        mycoll=mydb[input.replace(' ','_')+'_Tweets']
        dict=tweets_df.to_dict('records')
        if dict:
            mycoll.insert_many(dict) 
            timestmp = time.time()
            mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": input+str(timestmp)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database')
            st.balloons()
        else:
            st.warning('Data Can\'t be uploaded as there is no tweets')
if csv:
    st.success("Data Downloaded in .csv")  
if json:
    st.success("Data Downloaded in .json")     
if disp:
    st.success("Data(Scraped) :")
    st.write(tweets_df)
if disp1:
    st.success("Accomplished!!!!")
    st.balloons()
    st.write(tweets_df)
