from __future__ import annotations

import aiohttp

from osrparse import Replay

from pathlib import Path

http: aiohttp.ClientSession

username: str
password: str
local_name: str
data_folder: Path
replay_folder: Path
avatar: Path | bytes
scores: dict[str, Replay] = {}