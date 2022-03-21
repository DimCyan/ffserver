from pathlib import Path
import fastapi
import aiofiles
import re

bucket_path = Path("__file__").parent.joinpath("bucket")


async def syspath(url_path: str = fastapi.Path(...)) -> Path:
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


async def save_formfile(path: Path, file: fastapi.UploadFile):
    content = await file.read()
    async with aiofiles.open(path, "wb+") as f:
        await f.write(content)
