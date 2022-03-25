#!/usr/bin/env python

import os
os.system(
    'cls' if os.name == 'nt' else 'clear'
)

import hashlib
from pathlib import Path

import aiohttp
import uvicorn
from fastapi import FastAPI

import cho
import web
import ava
import maps
import config

from ext import glob

app = FastAPI()

@app.on_event('startup')
async def start_up() -> None:
    glob.http = aiohttp.ClientSession()

    glob.username = config.bancho_username
    glob.password = hashlib.md5(
        config.bancho_password.encode()
    ).hexdigest()

    temp_path = Path(config.avatar)
    if temp_path.exists() and temp_path.is_file():
        config.avatar = temp_path
        return
    else:
        async with glob.http.get(config.avatar) as resp:
            if not resp or resp.status != 200:
                config.avatar = b''
        
            if not (content := await resp.content.read()):
                config.avatar = b''
            
            config.avatar = content
            return

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

if __name__ == '__main__':
    uvicorn.run(
        app, # type: ignore
        host = '127.0.0.1',
        port = 5000
    )