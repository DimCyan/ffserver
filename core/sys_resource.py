from pathlib import Path
import fastapi
import aiofiles
import re
import mimetypes

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


def check_name(name: str) -> bool:
    return not re.search(r'[\\\/\:\*\?\"\<\>\|]', name)


def get_mime(file: Path) -> str:
    return mimetypes.guess_type(file.name)[0]


async def read(file: Path) -> bytes:
    async with aiofiles.open(file,'rb') as f:
        return await f.read()


async def write(path: Path, content:bytes):
    async with aiofiles.open(path, "wb+") as f:
        await f.write(content)
