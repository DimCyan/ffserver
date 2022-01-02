import math
import os

__basedir__ = os.path.dirname(os.path.abspath("__file__"))
bucket_path = os.path.join(__basedir__, "bucket")
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


async def _gen_type(file_path: str) -> str:
    if os.path.isdir(file_path):
        return "📁"
    else:
        return some_types.get(os.path.splitext(file_path)[1], "❓")


async def _gen_size(file_path: str) -> str:
    fsize = os.path.getsize(file_path)
    fsize = fsize / float(1024 * 1024)
    return str(round(fsize, 2)) + "MB"


async def _gen_mtime(file_path: str) -> str:
    t = math.floor(os.path.getmtime(file_path))
    return str(t)


async def get_list(folder_path: str):
    name_list: list = os.listdir(folder_path)
    path_list: list = [os.path.join(folder_path, _) for _ in name_list]
    type_list: list = [await _gen_type(_) for _ in path_list]
    size_list: list = [await _gen_size(_) for _ in path_list]
    mtime_list: list = [await _gen_mtime(_) for _ in path_list]
    return [{"file_name": name_list[_],
             "type": type_list[_],
             "size": size_list[_],
             "modify_time": mtime_list[_]} for _ in range(len(name_list))]
