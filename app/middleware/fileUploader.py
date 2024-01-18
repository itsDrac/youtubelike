from datetime import datetime
from pathlib import Path
from fastapi import UploadFile


async def save_file_on_disk(file: UploadFile):
    temp_file_name = f"{str(datetime.now())}-{file.filename}"
    temp_file_name = Path.cwd().joinpath("public", "temp", temp_file_name)
    content = await file.read()
    temp_file_name.touch()
    temp_file_name.write_bytes(content)
    return temp_file_name
