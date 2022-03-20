from pathlib import Path
import fastapi
import mimetypes
import re
import aiofiles

bucket_path = Path("__file__").parent.joinpath("bucket")


async def syspath(url_path: str = fastapi.Path(...)) -> Path:
    return bucket_path / Path('.' + url_path)


emoji_map = {
    'image': "🏞️",
    'video': "🎥",
    'audio/mid': "🎼",
    'audio/wav': "🎹",
    'audio': "🎵",
    'text/.*ml': "📑",  # xml/html
    'text/css': "📃",
    'text/x-python': "🐍",  # py
    'text/plain': "📝",
    'text': "📄",
    'application/.*download': "🕹",  # exe
    'application/json': "🧾",
    'application/javascript': "📜",  # js
    'application/x-tar': "📦",
    'application/x-zip-compressed': "📦",
    'application/pdf': "📔",  # pdf
    'application/msword': "📘",  # doc
    'application/vnd.*\\.document': "📘",  # docx
    'application/vnd.ms-excel': "📗",  # xls/csv
    'application/vnd.*\\.sheet': "📗",  # xlsx
    'application/vnd.ms-powerpoint': "📙",  # ppt
    'application/vnd.*\\.presentation': "📙",  # pptx
    'application/x-x509-ca-cert': "📖",  # crt/cer
    'application/x-shockwave-flash': "📰",  # swf
}


def match_emoji(file: Path) -> str:
    if mime := mimetypes.guess_type(file.name)[0]:
        for type, emoji in emoji_map.items():
            if re.match(type, mime):
                return emoji
    return "❓"


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
