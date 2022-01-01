from fastapi import APIRouter, Request
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os.path
from .bucket_method import bucket_path, get_list

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("{rest_of_path:path}")
async def get_dir_list(request: Request, rest_of_path: str = None):
    """
    :return: [{file_name: "", type: "", size: "", modify_time: ""}]
    """
    real_path = os.path.join(bucket_path, *list(filter(None, rest_of_path.split('/'))))
    if os.path.isdir(real_path):
        return templates.TemplateResponse("bucket.html", {"request": request, "obj_list": await get_list(real_path)})
    else:
        filename = list(filter(None, rest_of_path.split('/')))[-1]
        return FileResponse(real_path, filename=filename)
