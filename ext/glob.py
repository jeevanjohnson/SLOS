from __future__ import annotations

import aiohttp

from pathlib import Path

http: aiohttp.ClientSession

username: str
password: str
avatar: Path | bytes