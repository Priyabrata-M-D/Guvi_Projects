from pymongo import MongoClient


# Define a function to upload data to MongoDB
def upload_to_mongodb(data, mongodb_conn_str, db_name, collection_name):
    # Connect to MongoDB
<<<<<<<<< Temporary merge branch 1
    mongodb_conn_str=('mongodb://localhost:27017')
=========
>>>>>>>>> Temporary merge branch 2
    client = MongoClient(mongodb_conn_str)
    db = client[db_name]
    collection = db[collection_name]
    # Convert data to a list of dictionaries
    data_dict = data.to_dict('records')
    # Insert data into MongoDB
    result = collection.insert_many(data_dict)
    return result
