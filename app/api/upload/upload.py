from fastapi import APIRouter, File, UploadFile
from . import upload_methods

router = APIRouter()


@router.post("/uploader")
async def upload_file(file: UploadFile = File(...)):
    file_size = await upload_methods.read_file(file=file)
    return file_size
