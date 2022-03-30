from pathlib import Path

from osrparse import Replay
from osrparse import Mod as Mods

from ext import glob

INVALID_MODS = Mods.Autopilot | Mods.Relax | Mods.Autoplay | Mods.Cinema | Mods.Target

def from_replay(replay: Path) -> None:
    score = Replay.from_string(
        replay.read_bytes()
    )

    if score.username != glob.local_name:
        return

    if score.mods & INVALID_MODS:
        return
    
    if not score.mods & Mods.NoFail:
        if score.life_bar_graph is None:
            return
        
        for bar in score.life_bar_graph:
            if bar.life == 0.0:
                return
    
    new_replay_path = glob.data_folder / f'{score.beatmap_hash}+{score.replay_hash}.osr'
    new_replay_path.write_bytes(replay.read_bytes())

    #glob.scores[score.beatmap_hash] = score

async def gather_all_scores() -> None:
    from osrparse import Replay

    for file in glob.data_folder.glob('*'):
        bmap_md5 = file.name.split('+', maxsplit=1)[0]
        glob.scores[bmap_md5] = Replay.from_string(
            file.read_bytes()
        )