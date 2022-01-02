from fastapi import APIRouter, File, UploadFile, Form
from . import upload_methods

router = APIRouter()


@router.post("/uploader")
async def upload_file(rest_path: str = Form(...), file: UploadFile = File(...)):
    file_size = await upload_methods.read_file(rest_path=rest_path, file=file)
    return file_size
