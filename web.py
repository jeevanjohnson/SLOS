from fastapi import APIRouter
from fastapi.responses import Response
from fastapi.responses import RedirectResponse

import config

router = APIRouter()

DEFAULT_CHARTS = '\n'.join([
    "beatmapId:0|beatmapSetId:0|beatmapPlaycount:0|beatmapPasscount:0|approvedDate:0",
    "chartId:beatmap|chartUrl:https://osu.ppy.sh/b/0|chartName:Beatmap Ranking|rankBefore:|rankAfter:0|maxComboBefore:|maxComboAfter:0|accuracyBefore:|accuracyAfter:0|rankedScoreBefore:|rankedScoreAfter:0|ppBefore:|ppAfter:0|onlineScoreId:0",
    "chartId:overall|chartUrl:https://osu.ppy.sh/u/2|chartName:Overall Ranking|rankBefore:0|rankAfter:0|rankedScoreBefore:0|rankedScoreAfter:0|totalScoreBefore:0|totalScoreAfter:0|maxComboBefore:0|maxComboAfter:0|accuracyBefore:0|accuracyAfter:0|ppBefore:0|ppAfter:0|achievements-new:|onlineScoreId:0"
]).encode()

async def notHandled() -> Response:
    return Response(b'error: no')

for path in [
    '/web/lastfm.php',
    '/web/osu-rate.php',
    '/web/osu-error.php',
    '/difficulty-rating',
    '/web/osu-session.php',
    '/web/osu-markasread.php',
    '/web/osu-getfriends.php',
    '/web/bancho_connect.php',
    '/web/osu-getbeatmapinfo.php'
]:
    router.get(path)(notHandled)

@router.get('/web/osu-submit-modular-selector.php')
async def submitModular() -> Response:
    return Response(DEFAULT_CHARTS)

@router.get('/web/osu-osz2-getscores.php')
async def leaderboardHandler() -> Response:
    return Response(b'3|false')

@router.get('/web/osu-search.php')
async def osuSearch( 
    r: int, q: str,
    m: int, p: int
) -> RedirectResponse:
    # check params manually just incase
    # peppy uses this web handler in a later
    # update to send info for an anti-cheat 

    params = {
        'u': config.bancho_username,
        'h': config.bancho_password,
        'r': r,
        'q': q,
        'm': m,
        'p': p
    }
    
    bancho_url = (
        'https://osu.ppy.sh/web/osu-search.php?' +
        '&'.join([f'{k}={v}' for k, v in params.items()])
    )

    return RedirectResponse(bancho_url)

@router.get('/d/{set_id}')
async def download(
    set_id: int
) -> RedirectResponse:
    return RedirectResponse(f'https://osu.gatari.pw/d/{set_id}')