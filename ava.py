from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import Response

from ext import glob

router = APIRouter()

@router.get('/{user_id}')
async def avatar(
    user_id: int
) -> Response:
    if user_id != 2:
        async with glob.http.get(
            f'https://a.ppy.sh/{user_id}?.png'
        ) as resp:
            return Response(await resp.content.read())

    if isinstance(glob.avatar, Path):
        return Response(glob.avatar.read_bytes())
    
    return Response(glob.avatar)