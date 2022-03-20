from fastapi import APIRouter, Request
from starlette.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from core.bucket_method import get_real_path, get_list

bucket = APIRouter()
templates = Jinja2Templates(directory="templates")


@bucket.get("{rest_of_path:path}", response_class=HTMLResponse, summary="Jinja2Templates Page")
async def get_dir_list(request: Request, rest_of_path: str = None):
    """
    :return: [{file_name: "", type: "", size: "", modify_time: ""}]
    """
    real_path = get_real_path(rest_of_path=rest_of_path)
    if real_path.is_dir():
        return templates.TemplateResponse("bucket.html", {"request": request, "obj_list": get_list(real_path)})
    else:
        return FileResponse(real_path, filename=real_path.name)
