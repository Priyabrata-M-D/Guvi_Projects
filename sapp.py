import streamlit as st
import pandas as pd
import pymongo
from tscrape import scrape_twitter_data

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://PriyabrataDS:uwm4jJEcPYC1r0oV@cluster1.j9x92do.mongodb.net/test")
db = client['trial']
test = db['Test']
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")


# Define a function to upload data to MongoDB
def upload_to_mongodb(data):
    # Insert data into MongoDB
    result = test.insert_many(data.to_dict('records'))
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
            # Upload data to MongoDB
            upload_to_mongodb(tweets_df)
            st.success('Data uploaded to MongoDB.')

            # Display the uploaded data in a table
            st.write(pd.DataFrame(list(test.find())))

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
