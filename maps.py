from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/{file_path:path}")
async def everything(request: Request) -> RedirectResponse:
    path: str = request["path"].removeprefix("/b")

    return RedirectResponse(f"https://b.ppy.sh{path}", status_code=301)
