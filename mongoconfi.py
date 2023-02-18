from pymongo import MongoClient


# Define a function to upload data to MongoDB
def upload_to_mongodb(data, mongodb_conn_str, twitter_scraping, scrapped):
    # Connect to MongoDB
    mongodb_conn_str=("mongodb+srv://dsa830dsa:Priy%408908@cluster0.o5d3gwp.mongodb.net/test")
    client = MongoClient(mongodb_conn_str)
    db = client[twitter_scraping]
    collection = db[scrapped]
    # Convert data to a list of dictionaries
    data_dict = data.to_dict('records')
    # Insert data into MongoDB
    result = collection.insert_many(data_dict)
    return result