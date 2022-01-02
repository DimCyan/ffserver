from fastapi import UploadFile
from app.api.get_obj.bucket_method import get_real_path


async def read_file(rest_path: str, file: UploadFile):
    dir_path = await get_real_path(rest_of_path=rest_path)
    content = await file.read()
    with open(f"{dir_path}/{file.filename}", "wb+") as f:
        f.write(content)
    return len(content)/1024
