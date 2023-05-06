# Twitter Scraping

This Interactive Streamlit GUI is designed to scrape Twitter data based on user input (i.e. keywords or hashtags) and store it in a NOSQL database. The data can then be displayed in a Streamlit app and downloadable in CSV and JSON format.

## Installation
To run this project, you will need to have the following installed:

* Python 3.x
* MongoDB
* The required Python packages (listed in requirements.txt)

## Usage
* Clone the repository to your local machine.
* Install the required Python packages by running pip install -r requirements.txt in your terminal.
* Set up a database connection (I am using mongodb here). You can also use MongoDB Atlas instead of local instance.
* In twitter_scrapper.py, enter your MongoDB database connection info.  or,
* Directly Run streamlit app using LInk provided for Application.
* Enter the hashtag/keyword, date range, and tweet count in the Streamlit app and click the "Scrape" button.
* You can click the "Download CSV" or "Download JSON" button to download the data in the respective format.
* To store data hit the button "Upload to database" or to show the scraped data hit 'show tweets'

## Files
* Source code is in twitter_scrape.py
* APP link: https://priyabrata-m-d-guvi-projects-twitter-scrape-on5bv1.streamlit.app/
