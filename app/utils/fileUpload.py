import os
import cloudinary
from pathlib import Path


cloudinary.config(
  cloud_name="dc7rie3n0",
  api_key=os.getenv("CLOUDINARY_API_KEY"),
  api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


async def upload_on_cloudinary(localpath: Path):
    try:
        if not localpath:
            return
        # Upload the file in Cloudinary
        result = await cloudinary.uploader.upload(str(localpath), resource_type="auto")
        print("File is uploaded in cloudinary: ", result)
        return result

    except Exception:
        localpath.unlink(True)
