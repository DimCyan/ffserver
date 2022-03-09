from fastapi import APIRouter, File, UploadFile, Form, Request
from core import upload_method

router = APIRouter()


@router.post("/uploader")
async def upload_file(request: Request, rest_path: str = Form(default='/'), file: UploadFile = File(...)):
    file_size = await upload_method.read_file(rest_path=rest_path, file=file)
    return file_size
