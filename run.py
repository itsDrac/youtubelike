import os
import uvicorn
from app import app as api

if __name__ == "__main__":
    port = int(os.getenv("PORT")) or 8000
    uvicorn.run(api, port=port)
