from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

def dBConnection():
    try:
        load_dotenv()
        
        # LOADING MONGODB CONNECTION INFO FROM ENVIRONMENT VARIABLES
        mongo_url = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        collection_prediction = os.getenv("COLLECTION_FOR_PREDICTION")
        collection_feedback = os.getenv("COLLECTION_FOR_FEEDBACK")
        collection_instructions = os.getenv("COLLECTION_FOR_INSTRUCTIONS")
        
        # CREATING A MONGODB CLIENT AND CONNECT TO THE DATABASE
        client = MongoClient(mongo_url, server_api=ServerApi('1'))
        db = client[db_name]
        
        # GETTING THE COLLECTIONS BASED ON ENVIRONMENT VARIABLE SETTINGS
        collection_pred = db[collection_prediction]
        collection_feedback = db[collection_feedback]
        collection_instructions = db[collection_instructions]
        
        # CHECKING IF THE CONNECTION IS SUCCESSFUL
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        # RETURN CLIENT, DB, AND COLLECTIONS AS NEEDED
        return collection_pred, collection_instructions, collection_feedback 

    except Exception as e:
        print("Failed to connect to MongoDB:", e)
