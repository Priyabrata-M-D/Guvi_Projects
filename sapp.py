import streamlit as st
from tscrape import scrape_twitter_data
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_scraping']
collection = db['scrapped']


# Define a function to upload data to MongoDB
def upload_to_mongodb(data, collection):
    # Convert data to a list of dictionaries
    data_dict = data.to_dict('records')
    # Insert data into MongoDB
    result = collection.insert_many(data_dict)
    # Display result
    st.write(f'{len(result.inserted_ids)} documents uploaded to MongoDB')
    return result


# Define the Streamlit app
def main():
    # Page title
    st.title('Twitter Scraper')

    # Get user input
    hashtag = st.text_input('Hashtag/Keyword')
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')
    max_tweets = st.number_input('Max Tweets')

    # Scrape Twitter data
    if st.button('Scrape'):
        tweets_df = scrape_twitter_data(hashtag, start_date, end_date, max_tweets)

        # Display data in a table
        st.write(tweets_df)

        # Upload data to MongoDB
        if st.button('Upload to MongoDB'):
            result = upload_to_mongodb(tweets_df, collection)
            # Display result
            st.write(f'{len(result.inserted_ids)} documents uploaded to MongoDB')

         # Download data in CSV format
        st.download_button('Download CSV',
                           tweets_df.to_csv(),
                           file_name='twitter_scrape.csv',
                           mime="text/csv")

        # Download data in JSON format
        st.download_button('Download JSON',
                           tweets_df.to_json(),
                           file_name='twitter_scrape.json',
                           mime="text/json")


if __name__=='__main__':
    main()
