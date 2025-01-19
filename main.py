from fastapi import FastAPI,Request
from routers import auth, versions
from database import Base, engine
import logging
import re
import time 



# Initialize the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

@app.middleware("http") 
async def log_requests(request: Request, call_next):
     logger.info(f"Request: {request.method} {request.url}") 
     start_time = time.time() 
     response = await call_next(request) 
     process_time = time.time() - start_time 
     logger.info(f"Response: {response.status_code} (time: {process_time:.4f}s)") 
     return response

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(versions.router, prefix="/versions", tags=["Version Management"])

@app.get("/")
def root():
    return {"message": "Welcome to OTG"}
