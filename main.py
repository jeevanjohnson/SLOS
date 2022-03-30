#!/usr/bin/env python

import os
import hashlib
import asyncio
from pathlib import Path

import psutil
import aiohttp
import uvicorn
from fastapi import FastAPI

import cho
import web
import ava
import maps
import scores
import config

from ext import glob

if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

app = FastAPI()

@app.on_event('startup')
async def start_up() -> None:
    glob.http = aiohttp.ClientSession()

    glob.username = config.bancho_username
    glob.password = hashlib.md5(
        config.bancho_password.encode()
    ).hexdigest()

    glob.local_name = config.ingame_name

    temp_path = Path(config.avatar)
    if temp_path.exists() and temp_path.is_file():
        glob.avatar = temp_path
    else:
        async with glob.http.get(config.avatar) as resp:
            if not resp or resp.status != 200:
                glob.avatar = b''
        
            if not (content := await resp.content.read()):
                glob.avatar = b''
            
            glob.avatar = content
    
    glob.data_folder = Path.cwd() / '.data'
    if not glob.data_folder.exists():
        glob.data_folder.mkdir(exist_ok=True)
    
    asyncio.create_task(osuHandler())

@app.on_event('shutdown')
async def shutdown() -> None:
    await glob.http.close()

async def osuHandler() -> None:
    osu = None
    while await asyncio.sleep(
        delay = 0.2, 
        result = True
    ):
        # find osu!.exe and gather the replay folder path from it
        if not osu:
            processes = [
                process for process in psutil.process_iter()
                if process.name() == 'osu!.exe'
            ]
            if not processes:
                continue
            
            osu = processes[0]
            osu_path = Path(osu.exe())

            glob.replay_folder = osu_path.parent / 'Replays'
            if not glob.replay_folder.exists():
                glob.replay_folder.mkdir(exist_ok=True)
            
            break
    
    def get_timestamp() -> float:
        return glob.replay_folder.stat().st_mtime

    last_changed = get_timestamp()
    while await asyncio.sleep(
        delay = 0.2, 
        result = True
    ):
        change = get_timestamp()

        if last_changed == change:
            continue
        
        last_changed = change

        replay = glob.replay_folder / max(
            glob.replay_folder.glob('*.osr'),
            key = os.path.getctime
        )

        if not replay.exists():
            continue

        scores.from_replay(replay)

def init_app(app: FastAPI) -> FastAPI:
    app.include_router(
        web.router, 
        prefix = '/osu'
    )

    for path in ('/c4', '/c5', '/c6', '/ce', '/c'):
        app.include_router(
            cho.router,
            prefix = path
        )

    app.include_router(
        ava.router,
        prefix = '/a'
    )

    app.include_router(
        maps.router,
        prefix = '/b'
    )

    return app

app = init_app(app)

def main() -> int:
    uvicorn.run(
        "main:app",
        host = '127.0.0.1',
        port = 5000,
        reload = True
    )

    return 0

if __name__ == '__main__':
    raise SystemExit(main())