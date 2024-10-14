import os
from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger
from config.log_config import setup_logging
from app.routes import router as api_router

# Load environment variables
load_dotenv()

# Set up logging
setup_logging()

# Load burr path
# The path to the burr directory is stored in an environment variable (in this example, set in docker-compose.yml)
BURR_PATH = os.getenv("burr_path")

# Create the FastAPI app
app = FastAPI()


# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


# CORS
# CORS settings are not needed since we only accept requests from an application or Postman, not from a browser.
# Add CORS middleware to allow requests from browsers

# Include the API router
app.include_router(api_router, prefix="/api")

# Log where the server is running
logger.info("Server running at http://0.0.0.0:8000")
