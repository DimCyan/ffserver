from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from starlette.responses import FileResponse
from core import sysfile
import pathlib
from . import schemas
from datetime import datetime

file = APIRouter(tags=["file"])


@file.get("{url_path:path}", response_class=FileResponse, summary="download")
async def download_file(path: pathlib.Path = Depends(sysfile.syspath)):
    if path.is_file():
        return FileResponse(path, filename=path.name)
    raise HTTPException(status_code=404)


@file.post("{url_path:path}", response_model=schemas.sys_file, summary="upload")
async def upload_file(path: pathlib.Path = Depends(sysfile.syspath), file: UploadFile = File(...)):
    if not path.is_dir():
        raise HTTPException(status_code=404)
    new_file = path / pathlib.Path(file.filename)
    if new_file.is_file():
        raise HTTPException(status_code=412, detail="File already exists")
    if not sysfile.check_name(file.filename):
        raise HTTPException(status_code=422, detail="Dirname cannot contain \/:*?<>|")
    await sysfile.save_formfile(new_file, file)
    return schemas.sys_file(
        name=new_file.name,
        mtime=datetime.fromtimestamp(
            pathlib.Path.stat(new_file).st_mtime),
        size=sysfile.format_bytes_size(new_file)
    )
    
    