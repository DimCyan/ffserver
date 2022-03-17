from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pathlib import Path
from api import bucket, upload

app = FastAPI()

app.mount("/static", StaticFiles(directory=Path(__file__).parent.joinpath("static")), name="static")

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(bucket.router, prefix="/bucket", tags=["bucket"])


@app.get('/')
def index():
    return RedirectResponse(url='/bucket')


if __name__ == '__main__':
    import os
    os.system('')
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8010, reload=True, debug=True)
