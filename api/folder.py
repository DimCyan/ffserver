from fastapi import APIRouter, Depends, Form, HTTPException
from . import schemas
from core import sys_resource
import pathlib
from datetime import datetime
from typing import Union

folder = APIRouter(tags=["folder"])


@folder.get("{url_path:path}", response_model=list[Union[schemas.sys_folder, schemas.sys_file]], summary="ls")
async def get_folder_dir(path: pathlib.Path = Depends(sys_resource.syspath)):
    if not path.is_dir():
        raise HTTPException(status_code=404)
    ls = []
    for _ in path.iterdir():
        if _.is_dir():
            ls.append(schemas.sys_folder(
                name=_.name,
                mtime=datetime.fromtimestamp(pathlib.Path.stat(_).st_mtime)
            ))
        else:
            ls.append(schemas.sys_file(
                name=_.name,
                mtime=datetime.fromtimestamp(
                    pathlib.Path.stat(_).st_mtime),
                size=sys_resource.format_bytes_size(_)
            ))
    return ls
    


@folder.post("{url_path:path}", response_model=schemas.sys_folder, summary="mkdir")
async def create_folder(path: pathlib.Path = Depends(sys_resource.syspath), dirname: str = Form(...)):
    if not path.is_dir():
        raise HTTPException(status_code=404)
    dirname = dirname.strip()
    if not dirname:
        raise HTTPException(status_code=422, detail="Dirname cannot be a blank string")
    if not sys_resource.check_name(dirname):
        raise HTTPException(status_code=422, detail="Dirname cannot contain \/:*?<>|")
    try:
        new_dir = path / pathlib.Path(dirname)
        new_dir.mkdir(parents=False, exist_ok=False)
        return schemas.sys_folder(
            name=dirname,
            mtime=datetime.fromtimestamp(pathlib.Path.stat(new_dir).st_mtime))
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except FileExistsError:
        raise HTTPException(status_code=412, detail="Directory already exists")
    
