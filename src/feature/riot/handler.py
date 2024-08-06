from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.feature.riot.client import RiotServices, RiotClientException
from src.core.dependency import get_riot_services, get_logged_user

from .responses import RiotSummonerResponse

router = APIRouter(prefix="/riot")


@router.get("/summoner/by-riot-id", response_model=RiotSummonerResponse, dependencies=[Depends(get_logged_user)])
async def get_summoner_by_riot_id(
    game_name: str = Query(), tag_line: str = Query(), riot_services: RiotServices = Depends(get_riot_services)
):
    try:
        account = riot_services.account.by_riot_id(game_name, tag_line)
        return riot_services.summoner.by_puuid(account["puuid"])
    except RiotClientException as e:
        return JSONResponse(e.data, status_code=e.status_code)
