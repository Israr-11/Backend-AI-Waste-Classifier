from datetime import datetime, time
from typing import Optional
from fastapi import HTTPException
from utils.database import dBConnection

def get_prediction_stats(date: Optional[datetime] = None, 
                        category: Optional[str] = None) -> dict:
    try:
        collection_pred, collection_instructions, collection_feedback = dBConnection()
        
        # Build query filters
        query = {}
        
        # Add single date filter if provided
        if date:
            # Set start to beginning of the specified date (00:00:00)
            start = datetime.combine(date.date(), time.min)
            # Set end to end of the specified date (23:59:59)
            end = datetime.combine(date.date(), time.max)
            query["entryTime"] = {"$gte": start, "$lte": end}
            
        # Add category filter if provided
        if category:
            query["category"] = category
            
        # Validate that we have at least one filter
        if not query:
            raise HTTPException(status_code=400, detail="At least one filter (date or category) must be provided")
            
        print(f"Query filter: {query}")
        
        # Get all matching predictions
        predictions = list(collection_pred.find(query))
        print(f"Found {len(predictions)} predictions")
        
        # Calculate statistics
        total_predictions = len(predictions)
        correct_predictions = sum(1 for pred in predictions 
                                if pred["original_prediction"] == pred["correct_classification"])
        incorrect_predictions = total_predictions - correct_predictions
        
        # Calculate category-wise breakdown
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
