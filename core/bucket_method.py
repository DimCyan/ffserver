import mimetypes
import re
from pathlib import Path

bucket_path = Path("__file__").parent.joinpath("bucket")

some_types = {
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


def get_real_path(rest_of_path: str) -> Path:
    return bucket_path / Path('.' + rest_of_path)


def _gen_type(file_path: Path) -> str:
    if file_path.is_dir():
        return "📁"
    else:
        if mime := mimetypes.guess_type(file_path.name)[0]:
            for type, emoji in some_types.items():
                if re.match(type, mime):
                    return emoji
        return "❓"


def _gen_size(file_path: Path) -> str:
    if file_path.is_dir():
        return ''
    fsize = Path.stat(file_path).st_size
    series = ['B', 'KB', 'MB', 'GB', 'TB']
    for _ in series:
        if fsize < 1024:
            return f"{fsize:.4g}{_}"  # reserve 4 significant digits
        fsize /= 1024


def _gen_mtime(file_path: Path) -> str:
    return f'{Path.stat(file_path).st_mtime // 1}'


def get_list(folder_path: Path):
    return [{"file_name": _.name,
             "type": _gen_type(_),
             "size": _gen_size(_),
             "modify_time": _gen_mtime(_)} for _ in folder_path.iterdir()]
