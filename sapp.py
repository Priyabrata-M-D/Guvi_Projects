import json
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from tscrape import scrape_twitter_data


# Define a function to upload data to MongoDB
def upload_to_mongodb(json_file):
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://dsa830dsa:Priy%408908@cluster0.o5d3gwp.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    collection = db.tscrapped
    # Convert data to JSON records and Insert data into MongoDB
    with open(json_file, 'r') as f:
        data = json.load(f)
    result = collection.insert_many(data)

    # Retrieve the uploaded data from MongoDB
    uploaded_data = list(collection.find())

    return uploaded_data


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

        # Create JSON file
        json_file = 'tweets.json'
        tweets_df.to_json(json_file, orient='records')

        # Display data in a table
        st.write(tweets_df)

        # Upload data to MongoDB
        if st.button('Upload to MongoDB'):
            uploaded_data = upload_to_mongodb(json_file)
            # Display result
            st.write(f'{len(uploaded_data)} documents uploaded to MongoDB')
            # Display the uploaded data in a table
            st.write(pd.DataFrame(uploaded_data))

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


if __name__ == '__main__':
    main()
