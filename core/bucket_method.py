import math
from pathlib import Path

bucket_path = Path("__file__").parent.joinpath("bucket")

some_types = {
    ".png": "🏞️",
    ".dwg": "🏞️",
    ".xcf": "🏞️",
    ".jpg": "🏞️",
    ".jpx": "🏞️",
    ".gif": "🏞️",
    ".webp": "🏞️",
    ".cr2": "🏞️",
    ".tif": "🏞️",
    ".bmp": "🏞️",
    ".jxr": "🏞️",
    ".psd": "🏞️",
    ".ico": "🏞️",
    ".heic": "🏞️",
    ".3gp": "🎥",
    ".mp4": "🎥",
    ".m4v": "🎥",
    ".mkv": "🎥",
    ".webm": "🎥",
    ".mov": "🎥",
    ".avi": "🎥",
    ".wmv": "🎥",
    ".mpg": "🎥",
    ".flv": "🎥",
    ".aac": "🎵",
    ".mid": "🎵",
    ".mp3": "🎵",
    ".m4a": "🎵",
    ".ogg": "🎵",
    ".flac": "🎵",
    ".wav": "🎵",
    ".amr": "🎵",
    ".aiff": "🎵",
    ".br": "📦",
    ".rpm": "📦",
    ".dcm": "📦",
    ".epub": "📦",
    ".zip": "📦",
    ".tar": "📦",
    ".rar": "📦",
    ".gz": "📦",
    ".bz2": "📦",
    ".7z": "📦",
    ".xz": "📦",
    ".pdf": "📦",
    ".exe": "📦",
    ".swf": "📦",
    ".rtf": "📦",
    ".eot": "📦",
    ".ps": "📦",
    ".sqlite": "📦",
    ".nes": "📦",
    ".crx": "📦",
    ".cab": "📦",
    ".deb": "📦",
    ".ar": "📦",
    ".Z": "📦",
    ".lzo": "📦",
    ".lz": "📦",
    ".lz4": "📦",
    ".txt": "📄",
    ".py": "🐍",
    ".rb": "💎"
}


async def get_real_path(rest_of_path: str) -> Path:
    print(rest_of_path)
    return bucket_path / Path('.' + rest_of_path)


def _gen_type(file_path: Path) -> str:
    if file_path.is_dir():
        return "📁"
    else:
        return some_types.get(file_path.name, "❓")


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
