import os
import cloudinary
import cloudinary.uploader
from pathlib import Path
# from datetime import datetime
from fastapi import UploadFile, HTTPException

from dotenv import load_dotenv
load_dotenv()


cloudinary.config(
    cloud_name="dc7rie3n0",
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


async def save_file_on_disk(file: UploadFile) -> Path:
    try:
        temp_file_name = Path(f"public/temp/{file.filename}")
        temp_file_name.touch()
        content = await file.read()
        temp_file_name.write_bytes(content)

    except Exception:
        raise HTTPException(status_code=500, detail="Unable to upload in server")
    return temp_file_name


async def upload_on_cloudinary(localpath: Path):
    try:
        if not localpath:
            return
        # Upload the file in Cloudinary
        result = cloudinary.uploader.upload(str(localpath), resource_type="auto")
        print("File is uploaded in cloudinary: ", result)
        # Needed: result.url
        return result

    except Exception:
        raise HTTPException(status_code=500, detail="Unable to upload from server")

    finally:
        localpath.unlink(True)
