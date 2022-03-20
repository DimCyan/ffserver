from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pathlib import Path
import api

app = FastAPI(title='FFServer', description="""
    It's not safe at all. Use it on your home WLAN.
""")

app.mount("/static", StaticFiles(directory=Path(__file__).parent.joinpath("static")), name="static")

app.include_router(api.bucket, prefix="/bucket", tags=["bucket"])
app.include_router(api.file, prefix="/file")
app.include_router(api.folder, prefix="/folder")


@app.get('/')
def index():
    return RedirectResponse(url='/bucket')


if __name__ == '__main__':
    import os
    os.system('')
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8010, reload=True, debug=True)
