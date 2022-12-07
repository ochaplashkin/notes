from starlette.responses import HTMLResponse
from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/")
async def health() -> HTMLResponse:
    html_content = """
    <link id="favicon" rel="icon" type="image/x-icon" href="static/images/favicon.ico">
    <html>
        <head>
            <title>Notes</title>
        </head>
        <body>
            <h1>Index page</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
