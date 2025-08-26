from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional
from services.statsService import get_prediction_stats

router = APIRouter()

@router.get("/prediction-stats")
async def get_stats(
    date: Optional[datetime] = Query(None, description="Date to filter by (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Category to filter by")
):
    return get_prediction_stats(date, category)
