"""API

- bucket: Jinja2 Page
- file: RESTful api
- folder: RESTful api

"""

__all__ = ['bucket', 'file', 'folder']


from .bucket import bucket
from .file import file
from .folder import folder
