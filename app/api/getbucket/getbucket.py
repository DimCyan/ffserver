from fastapi import APIRouter
from starlette.responses import FileResponse
import os.path
from .bucket_method import bucket_path, get_list

router = APIRouter()


@router.get("/{rest_of_path:path}")
async def get_dir_list(rest_of_path: str = None):
    """
    :param rest_of_path:
    :return: [{file_name: "", type: "", size: "", modify_time: ""}]
    """
    real_path = os.path.join(bucket_path, *list(filter(None, rest_of_path.split('/'))))
    if os.path.isdir(real_path):
        return await get_list(real_path)
    else:
        filename = list(filter(None, rest_of_path.split('/')))[-1]
        return FileResponse(real_path, filename=filename)
