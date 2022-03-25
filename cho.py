from __future__ import annotations

from typing import Optional

from fastapi import Header
from fastapi import APIRouter
from fastapi.responses import Response

import config
import packets

router = APIRouter()

LOGIN_CONTENT = (
    packets.userID(2) + 
    packets.notification('welcome to the better offline experience!') +
    packets.protocolVersion() +
    packets.friendsList(0) +
    packets.channelInfo('#osu', 'x', 1) +
    packets.channelInfoEnd() +
    packets.channelJoin('#osu') +
    packets.banchoPrivs(63) +
    packets.userStats(2, 0, '', '', 0, 0, 0, 0, 100.0, 0, 0, 0, 0) +
    packets.userPresence(2, config.ingame_name, 0, 0, 63, 0, (0, 0), 0)
)

LOGIN_RESPONSE = Response(
    LOGIN_CONTENT,
    headers = {'cho-token': 'x'}
)

@router.get('/')
async def cho(
    osu_token: Optional[str] = Header(None)
) -> Response:
    if not osu_token:
        return LOGIN_RESPONSE
    else:
        return Response()