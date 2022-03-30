import calendar
from typing import Any

from fastapi import Query
from fastapi import Request
from osrparse import Replay
from fastapi import APIRouter
from fastapi.responses import Response
from fastapi.responses import RedirectResponse

import config

from ext import glob

router = APIRouter()

DEFAULT_CHARTS = '\n'.join([
    "beatmapId:0|beatmapSetId:0|beatmapPlaycount:0|beatmapPasscount:0|approvedDate:0",
    "chartId:beatmap|chartUrl:https://osu.ppy.sh/b/0|chartName:Beatmap Ranking|rankBefore:|rankAfter:0|maxComboBefore:|maxComboAfter:0|accuracyBefore:|accuracyAfter:0|rankedScoreBefore:|rankedScoreAfter:0|ppBefore:|ppAfter:0|onlineScoreId:0",
    "chartId:overall|chartUrl:https://osu.ppy.sh/u/2|chartName:Overall Ranking|rankBefore:0|rankAfter:0|rankedScoreBefore:0|rankedScoreAfter:0|totalScoreBefore:0|totalScoreAfter:0|maxComboBefore:0|maxComboAfter:0|accuracyBefore:0|accuracyAfter:0|ppBefore:0|ppAfter:0|achievements-new:|onlineScoreId:0"
]).encode()

async def notHandled() -> Response:
    return Response(b'error: no')

def build_url(path: str, params: dict[str, Any]) -> str:
    return path + '&'.join([f'{k}={v}' for k, v in params.items()])

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
async def leaderboardHandler(
    request: Request,
    md5: str = Query(..., alias='c'),
) -> Response:
    params = request.query_params._dict.copy()
    if 'a' in params:
        del params['a']

    params['us'] = glob.username
    params['ha'] = glob.password

    async with glob.http.get(
        url = 'https://osu.ppy.sh/web/osu-osz2-getscores.php',
        params = params,
        headers = {'User-Agent': 'osu!'}
    ) as resp:
        raw_leaderboard = await resp.content.read()
    
    if not raw_leaderboard:
        return Response(b'error: no')
    
    leaderboard = raw_leaderboard.split(b'\n')

    scores = [
        Replay.from_string(s.read_bytes()) for s in
        glob.data_folder.glob(f'{md5}+*.osr')
    ]

    if not scores:
        leaderboard[4] = b''
        return Response(b'\n'.join(leaderboard))

    scores.sort(
        key = lambda s: s.score,
        reverse = True
    )

    best, = scores

    epoch_time = calendar.timegm(
        best.timestamp.utctimetuple()
    )

    leaderboard[4] = (
        f"{-best.replay_id}|{best.username}|{best.score}|"
        f"{best.max_combo}|{best.count_50}|{best.count_100}|"
        f"{best.count_300}|{best.count_miss}|{best.count_katu}|"
        f"{best.count_geki}|{int(best.perfect)}|{int(best.mods)}|2|"
        f"0|{epoch_time}|1"
        # num on lb, time, replay avaliable
    ).encode()

    return Response(b'\n'.join(leaderboard))

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