from pymongo import MongoClient
import json

# Define a function to upload data to MongoDB
def upload_to_mongodb(data, mongodb_conn_str, db_name, collection_name):
    # Connect to MongoDB
    mongodb_conn_str=()
    client = MongoClient('mongodb://localhost:27017')
    db = client["twitter_scrapping"]
    collection = db["scrapped"]
    # Convert data to a list of dictionaries
    data_dict = data.to_dict('records')
    # Convert data to JSON records
    data_json = json.dumps(data_dict)
    # Insert data into MongoDB
    result = collection.insert_many(data_dict)
    return result
