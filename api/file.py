from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from starlette.responses import FileResponse
from core import sys_resource
import pathlib
from . import schemas
from datetime import datetime

file = APIRouter(tags=["file"])


@file.get("{url_path:path}", response_class=FileResponse, summary="download")
async def download_file(path: pathlib.Path = Depends(sys_resource.syspath)):
    """download file"""
    if path.is_file():
        return FileResponse(path, filename=path.name)
    raise HTTPException(status_code=404)


@file.post("{url_path:path}", response_model=schemas.sys_file, summary="upload")
async def upload_file(path: pathlib.Path = Depends(sys_resource.syspath), file: UploadFile = File(...)):
    """upload file to specified folder"""
    if not path.is_dir():
        raise HTTPException(status_code=404)
    new_file = path / pathlib.Path(file.filename)
    if new_file.is_file():
        raise HTTPException(status_code=412, detail="File already exists")
    if not sys_resource.check_name(file.filename):
        raise HTTPException(status_code=422, detail="Dirname cannot contain \/:*?<>|")
    await sys_resource.save_formfile(new_file, file)
    return schemas.sys_file(
        name=new_file.name,
        mime=sys_resource.get_mime(new_file),
        mtime=datetime.fromtimestamp(
            pathlib.Path.stat(new_file).st_mtime),
        ctime=datetime.fromtimestamp(
            pathlib.Path.stat(new_file).st_ctime),
        size=sys_resource.format_bytes_size(new_file)
    )


@file.delete("{url_path:path}", summary="rm -f")
async def remove_file(path: pathlib.Path = Depends(sys_resource.syspath)):
    """remove file"""
    if not path.is_file():
        raise HTTPException(status_code=404)
    try:
        pathlib.Path.unlink(path)
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except OSError as e:
        raise HTTPException(status_code=412, detail=f"{e}")
    