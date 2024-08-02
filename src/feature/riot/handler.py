from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from riotwatcher import LolWatcher, RiotWatcher, ApiError as RiotWatcherException
from src.core.dependency import get_riot_watcher, get_lol_watcher

router = APIRouter(prefix="/riot")


def __riot_watcher_error_response(e: RiotWatcherException) -> JSONResponse:
    return JSONResponse({"riot_error": e.response.json()}, status_code=e.response.status_code)


@router.get("/summoner/by-riot-id")
async def get_summoner_by_riot_id(
    game_name: str = Query(),
    tag_line: str = Query(),
    riot_watcher: RiotWatcher = Depends(get_riot_watcher),
    lol_watcher: LolWatcher = Depends(get_lol_watcher),
):
    try:
        account = riot_watcher.account.by_riot_id("americas", game_name, tag_line)
        return lol_watcher.summoner.by_puuid("br1", encrypted_puuid=account["puuid"])
    except RiotWatcherException as e:
        return __riot_watcher_error_response(e)
