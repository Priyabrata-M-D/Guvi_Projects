# Twitter Scraping
This project is designed to scrape Twitter data based on user input and store it in a MongoDB database. The data can then be displayed in a Streamlit app and downloaded in CSV and JSON format.

## Installation
To run this project, you will need to have the following installed:

* Python 3.x
* MongoDB
* The required Python packages (listed in requirements.txt)

## Usage
* Clone the repository to your local machine.
* Install the required Python packages by running pip install -r requirements.txt in your terminal.
* Set up a MongoDB database and collection to store the scraped data. You can do this by creating an account on MongoDB Atlas or by installing MongoDB locally.
* In scrape_twitter.py, enter your MongoDB database and collection information in the mongo_client and mongo_collection variables.
* Run streamlit run app.py in your terminal to launch the Streamlit app.
* Enter the hashtag/keyword, date range, and tweet count in the Streamlit app and click the "Scrape" button.
* The scraped data will be displayed in a table in the Streamlit app. You can click the "Download CSV" or "Download JSON" button to download the data in the respective format.

## Files
* tscrape.py: Python script to scrape Twitter data.
* sapp.py: Streamlit app to display the scraped data and allow users to download it in CSV and JSON format and Upload data to DB.
