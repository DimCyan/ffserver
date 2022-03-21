from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, RedirectResponse
from pathlib import Path
import api


app = FastAPI(title='FFServer API', description="""
    It's not safe at all. Use it on your home WLAN.
""")


app.include_router(api.file, prefix="/api/file")
app.include_router(api.folder, prefix="/api/folder")

@app.get('/', response_class=HTMLResponse, tags=["page"])
def index():
    return RedirectResponse(url='/index.html')

app.mount("/", StaticFiles(directory=Path(__file__).parent.joinpath("static")), name="static")


if __name__ == '__main__':
    import os
    os.system('')
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0",port=8010, reload=True, debug=True)
