from fastapi import FastAPI # , HTTPException
from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse, Response, HTMLResponse
from pathlib import Path
import api
# import core


app = FastAPI(title='FFServer API', description="""
    It's not safe at all. Use it on your home WLAN.
""")


app.include_router(api.file, prefix="/api/file")
app.include_router(api.folder, prefix="/api/folder")

'''
@app.get('/{static_file:path}',response_class=Response(headers={"Content-Disposition" :"inline"}), tags=["static"])
async def static(static_file:str):
    """ 
        parse `/` to `/index.html`

    """
    path = Path(__file__).parent.joinpath("static", static_file)
    if path.is_file():
        return FileResponse(path)
    path /= Path('index.html')
    if path.is_file():
        html = await core.sys_resource.read(path)
        return HTMLResponse(html.decode('utf-8'))
    raise HTTPException(status_code=404)
'''
app.mount("/", StaticFiles(directory=Path(__file__).parent.joinpath("static"), html=True))


if __name__ == '__main__':
    import os
    os.system('')
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8010, reload=True)
