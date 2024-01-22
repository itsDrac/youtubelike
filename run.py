import os
import uvicorn
from app import app as api

if __name__ == "__main__":
    port = int(os.getenv("PORT") or 8000)
    # TODO: Remove reload flag and run by passing api on depoloyment.
    uvicorn.run(api, port=port)
