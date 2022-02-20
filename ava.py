from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import Response

import config

router = APIRouter()

@router.get('/{user_id}')
async def avatar(
    user_id: int
) -> Response:
    if isinstance(config.avatar, Path):
        return Response(config.avatar.read_bytes())
    
    return Response(config.avatar)