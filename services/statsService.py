from datetime import datetime, time
from typing import Optional
from fastapi import HTTPException
from utils.database import dBConnection

def get_prediction_stats(date: Optional[datetime] = None, 
                        category: Optional[str] = None) -> dict:
    try:
        collection_pred, collection_instructions, collection_feedback = dBConnection()
        
        # BUILD QUERY FILTERS
        query = {}
        
        # ADDING SINGLE DATE FILTER IF PROVIDED
        if date:
            # SETTING START TO BEGINNING OF THE SPECIFIED DATE (00:00:00)
            start = datetime.combine(date.date(), time.min)
            # SETTING END TO END OF THE SPECIFIED DATE (23:59:59)
            end = datetime.combine(date.date(), time.max)
            query["entryTime"] = {"$gte": start, "$lte": end}

        # ADDING CATEGORY FILTER IF PROVIDED
        if category:
            query["category"] = category

        # VALIDATING THAT WE HAVE AT LEAST ONE FILTER
        if not query:
            raise HTTPException(status_code=400, detail="At least one filter (date or category) must be provided")
            
        print(f"Query filter: {query}")
        
        # GETTING ALL MATCHING PREDICTIONS
        predictions = list(collection_pred.find(query))
        print(f"Found {len(predictions)} predictions")

        # CALCULATING STATISTICS
        total_predictions = len(predictions)
        correct_predictions = sum(1 for pred in predictions 
                                if pred["original_prediction"] == pred["correct_classification"])
        incorrect_predictions = total_predictions - correct_predictions

        # CALCULATING CATEGORY-WISE BREAKDOWN
        category_stats = {}
        for pred in predictions:
            cat = pred["category"]
            if cat not in category_stats:
                category_stats[cat] = {
                    "total": 0,
                    "correct": 0,
                    "incorrect": 0
                }
            
            category_stats[cat]["total"] += 1
            if pred["original_prediction"] == pred["correct_classification"]:
                category_stats[cat]["correct"] += 1
            else:
                category_stats[cat]["incorrect"] += 1
        
        return {
            "total_predictions": total_predictions,
            "correct_predictions": correct_predictions,
            "incorrect_predictions": incorrect_predictions,
            "accuracy_rate": (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0,
            "category_wise_stats": category_stats,
        }
        
    except Exception as e:
        print(f"Error in stats service: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")
