from fastapi import UploadFile
from core.bucket_method import get_real_path
import aiofiles


async def read_file(rest_path: str, file: UploadFile):
    dir_path = await get_real_path(rest_of_path=rest_path)
    content = await file.read()
    async with aiofiles.open(f"{dir_path}/{file.filename}", "wb+") as f:
        await f.write(content)
    return len(content)/1024
