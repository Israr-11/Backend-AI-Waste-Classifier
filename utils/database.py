from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

def dBConnection():
    try:
        load_dotenv()
        
        # Load MongoDB connection info from environment variables
        mongo_url = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        collection_prediction = os.getenv("COLLECTION_FOR_PREDICTION")
        collection_feedback = os.getenv("COLLECTION_FOR_FEEDBACK")
        collection_instructions = os.getenv("COLLECTION_FOR_INSTRUCTIONS")
        
        # Create a MongoDB client and connect to the database
        client = MongoClient(mongo_url, server_api=ServerApi('1'))
        db = client[db_name]
        
        # Get the collections based on environment variable settings
        collection_pred = db[collection_prediction]
        collection_feedback = db[collection_feedback]
        collection_instructions = db[collection_instructions]
        
        # Check if the connection is successful
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        # Return client, db, and collections as needed
        return collection_pred, collection_instructions, collection_feedback 

    except Exception as e:
        print("Failed to connect to MongoDB:", e)
