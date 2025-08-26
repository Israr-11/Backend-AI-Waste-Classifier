from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.imageProcessingController import router 
from controllers.feedbackController import router as feedback_router
from controllers.statsController import router as stats_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ALLOWING ALL ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)  # MOUNTING THE ORDER ROUTER
app.include_router(feedback_router)  # MOUNTING THE FEEDBACK ROUTER
app.include_router(stats_router)  # MOUNTING THE STATS ROUTER

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app --reload")