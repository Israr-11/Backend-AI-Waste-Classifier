from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

# Connect to MongoDB Atlas
client = MongoClient(mongo_url, server_api=ServerApi('1'))
db = client[db_name]
collection = db["recycling_instruction"]  # Explicitly set collection name

# Recycling instructions data
instructions = [
    {
        "category": "plastic",
        "isWaste": "Yes",
        "instructions": "All plastics, including soft plastics like plastic food wraps and bags, are accepted in the recycling bin. Ensure items are clean, dry, and placed loosely in the bin.",
        "recyclable": "Yes"
    },
    {
        "category": "glass",
        "isWaste": "Yes",
        "instructions": "Rinse glass bottles and jars to remove any food or liquid residue before placing them in the recycling bin. Do not include ceramics or Pyrex.",
        "recyclable": "Yes"
    },
    {
        "category": "metal",
        "isWaste": "Yes",
        "instructions": "Clean and dry metal items such as tins, cans, and foil before placing them loosely in the recycling bin. Flattening them can save space.",
        "recyclable": "Yes"
    },
    {
        "category": "paper",
        "isWaste": "Yes",
        "instructions": "Ensure paper items are clean and dry before placing them loosely in the recycling bin. Magazines, newspapers, and office paper are accepted.",
        "recyclable": "Yes"
    },
    {
        "category": "organic",
        "isWaste": "Yes",
        "instructions": "Place food waste, coffee grounds, tea bags, and garden waste in the compost or brown bin. Do not include plastic, glass, or metal.",
        "recyclable": "Yes (Compostable)"
    },
    {
        "category": "trash",
        "isWaste": "Yes",
        "instructions": "Items that cannot be recycled should be disposed of in the general waste bin. This includes contaminated materials, non-recyclable plastics, and hygiene products.",
        "recyclable": "No"
    },
    {
        "category": "ewaste",
        "isWaste": "Yes",
        "instructions": "Electronic waste, including old phones, batteries, and appliances, should be taken to designated e-waste collection centers or retail stores with recycling points.",
        "recyclable": "Yes (Special Disposal Required)"
    }
]


# Insert data into MongoDB
try:
    result = collection.insert_many(instructions)
    print(f"Inserted {len(result.inserted_ids)} recycling instructions successfully!")
except Exception as e:
    print("Error inserting data:", e)
