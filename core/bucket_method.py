import math, mimetypes, re
from pathlib import Path

bucket_path = Path("__file__").parent.joinpath("bucket")

some_types = {
    'image': "🏞️",
    'video': "🎥",
    'audio': "🎵",
    'application/json': "📄",
    'application/x-tar': "📦",
    'application/x-zip-compressed': "📦",
    'text/x-python': "🐍", # 要写在text之前才能被匹配
    'text': "📄",
}


async def get_real_path(rest_of_path: str) -> Path:
    print(rest_of_path)
    return bucket_path / Path('.' + rest_of_path)


def _gen_type(file_path: Path) -> str:
    if file_path.is_dir():
        return "📁"
    else:
        if(mime := mimetypes.guess_type(file_path.name)[0]):
            for type, emoji in some_types.items():
                if(re.match(type, mime)):
                    return emoji
        return "❓"


def _gen_size(file_path: Path) -> str:
    fsize = Path.stat(file_path).st_size
    fsize /= float(1024 ** 2)
    return str(round(fsize, 2)) + "MB"


def _gen_mtime(file_path: Path) -> str:
    t = math.floor(Path.stat(file_path).st_mtime)
    return str(t)


async def get_list(folder_path: Path):
    return [{"file_name": _.name,
             "type": _gen_type(_),
             "size": _gen_size(_),
             "modify_time": _gen_mtime(_)} for _ in folder_path.iterdir()]
