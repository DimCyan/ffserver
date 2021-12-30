from fastapi import UploadFile


async def read_file(file: UploadFile):
    content = await file.read()
    with open(f"bucket/{file.filename}", "wb+") as f:
        f.write(content)
    return len(content)/1024
