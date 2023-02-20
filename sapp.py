import base64
import streamlit as st
from mongoconfi import upload_to_mongodb
from tscrape import scrape_twitter_data


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
            result = upload_to_mongodb(tweets_df)
            # Display result
            st.write(f'{len(result.inserted_ids)} documents uploaded to MongoDB')

        # Download data in CSV format
        csv = tweets_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown('### Download CSV File')
        href = f'<a href="data:file/csv;base64,{b64}" download="twitter_data.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Download data in JSON format
        json = tweets_df.to_json(orient='records')
        b64 = base64.b64encode(json.encode()).decode()
        st.markdown('### Download JSON File')
        href = f'<a href="data:file/json;base64,{b64}" download="twitter_data.json">Download JSON</a>'
        st.markdown(href, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
