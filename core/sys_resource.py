from pathlib import Path
import fastapi
import aiofiles
import re
import filetype
import mimetypes
from typing import Optional, Union
from functools import singledispatch

bucket_path = Path("__file__").parent.joinpath("bucket")


def syspath(url_path: str = fastapi.Path(...)) -> Path:
    return bucket_path / Path('.' + url_path)


def format_bytes_size(file: Path) -> str:
    bytes_size = Path.stat(file).st_size
    series = ['B', 'KB', 'MB', 'GB', 'TB']
    for _ in series:
        if bytes_size < 1024:
            return f"{bytes_size:.4g}{_}"  # reserve 4 significant digits
        bytes_size /= 1024
    return f'{bytes_size:.4g}PB'


def check_name(name: str) -> bool:
    return not re.search(r'[\\\/\:\*\?\"\<\>\|]', name)


def get_mime(file: Path) -> Optional[str]:
    if (type := filetype.guess(file)) is None:
        return mimetypes.guess_type(file.name)[0]
    return type.mime


async def read(file: Path) -> bytes:
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


@singledispatch
async def write(data: Union[str, bytes], file: Path):
    pass


@write.register(bytes)
async def _(data: bytes, file: Path):
    async with aiofiles.open(file, "wb+") as f:
        await f.write(data)


@write.register(str)
async def _(data: str, file: Path):
    async with aiofiles.open(file, "w+", encoding='utf-8') as f:
        await f.write(data)
