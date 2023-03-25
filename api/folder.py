from fastapi import APIRouter, Depends, Form, HTTPException
import shutil
from . import schemas
from core import sys_resource
import pathlib
from datetime import datetime
from typing import Union, List

folder = APIRouter(tags=["folder"])

LS = List[Union[schemas.sys_file, schemas.sys_folder]]


@folder.get("{url_path:path}", response_model=LS, summary="ls")
def get_folder_dir(path: pathlib.Path = Depends(sys_resource.syspath)):
    """get all file_stat_info in specified folder"""
    if not path.is_dir():
        raise HTTPException(status_code=404)
    ls :LS = []
    for _ in path.iterdir():
        if _.is_dir():
            ls.append(schemas.sys_folder(
                name=_.name,
                mtime=datetime.fromtimestamp(pathlib.Path.stat(_).st_mtime),
                ctime=datetime.fromtimestamp(pathlib.Path.stat(_).st_ctime))
            )
        else:
            ls.append(schemas.sys_file(
                name=_.name,
                mime=sys_resource.get_mime(_),
                mtime=datetime.fromtimestamp(pathlib.Path.stat(_).st_mtime),
                ctime=datetime.fromtimestamp(pathlib.Path.stat(_).st_ctime),
                size=sys_resource.format_bytes_size(_))
            )
    return ls
    

@folder.post("{url_path:path}", response_model=schemas.sys_folder, summary="mkdir")
def create_folder(path: pathlib.Path = Depends(sys_resource.syspath), dirname: str = Form(...)):
    """create a folder in specified folder"""
    if not path.is_dir():
        raise HTTPException(status_code=404)
    dirname = dirname.strip()
    if not dirname:
        raise HTTPException(status_code=422, detail="Name cannot be a blank string")
    if not sys_resource.check_name(dirname):
        raise HTTPException(status_code=422, detail=r"Name cannot contain \/:*?<>|")
    try:
        new_dir = path / pathlib.Path(dirname)
        new_dir.mkdir(parents=False, exist_ok=False)
        return schemas.sys_folder(
            name=dirname,
            mtime=datetime.fromtimestamp(pathlib.Path.stat(new_dir).st_mtime),
            ctime=datetime.fromtimestamp(pathlib.Path.stat(new_dir).st_ctime))
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except FileExistsError:
        raise HTTPException(status_code=412, detail="Name already exists")
    except OSError as e:
        raise HTTPException(status_code=412, detail=f"{e}")


@folder.put("{url_path:path}", summary="mv")
def move_folder(path: pathlib.Path = Depends(sys_resource.syspath), new_path: str = Form(...)):
    """set new path(new name)"""
    if not path.is_dir():
        raise HTTPException(status_code=404)
    try:
        path.rename(sys_resource.bucket_path / pathlib.Path("." + new_path))
    except FileExistsError:
        raise HTTPException(status_code=412, detail="Name already exists")
    except OSError as e:
        raise HTTPException(status_code=412, detail=f"{e}")


@folder.delete("{url_path:path}", summary="rm -rf")
def remove_folder(path: pathlib.Path = Depends(sys_resource.syspath)):
    """remove empty folder and non-empty folder"""
    if path == sys_resource.bucket_path:
        raise HTTPException(status_code=422, detail="Cannot remove root folder")
    """
    try:
        pathlib.Path.rmdir(path) # rm -f
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except OSError:
        raise HTTPException(status_code=412, detail="The folder is not empty")
    """
    try:
        shutil.rmtree(path) # rm -rf
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except OSError as e:
        raise HTTPException(status_code=412, detail=f"{e}")
