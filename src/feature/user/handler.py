from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.feature.riot.client import RiotClientException, RiotServices
from src.core.model import User, LeagueOfLegendsAccount, LeagueOfLegendsSummoner
from src.core.dependency import get_db, get_logged_user, get_riot_services

from .response import UserResponse, LeagueOfLegendsAccountResponse
from .payload import SetRiotPuuidPayload

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserResponse, tags=["Users"])
async def get_me(logged_user: User = Depends(get_logged_user)):
    return logged_user


@router.patch("/me/set-riot-puuid", response_model=LeagueOfLegendsAccountResponse, tags=["Users"])
async def set_riot_puuid(
    payload: SetRiotPuuidPayload,
    logged_user: User = Depends(get_logged_user),
    db: Session = Depends(get_db),
    riot_services: RiotServices = Depends(get_riot_services),
):
    if logged_user.league_of_legends_account != None:
        db.delete(logged_user.league_of_legends_account)
    try:
        lol_account = riot_services.account.by_puuid(payload.puuid)
        lol_summoner = riot_services.summoner.by_puuid(payload.puuid)
    except RiotClientException as e:
        return JSONResponse(e.data, status_code=e.status_code)
    account = LeagueOfLegendsAccount(
        lol_game_name=lol_account["game_name"],
        lol_tag_line=lol_account["tag_line"],
        lol_puuid=lol_account["puuid"],
        user=logged_user,
    )
    db.add(account)
    summoner = LeagueOfLegendsSummoner(
        lol_id=lol_summoner["id"],
        lol_account_id=lol_summoner["account_id"],
        lol_puuid=lol_summoner["puuid"],
        lol_profile_icon_id=lol_summoner["profile_icon_id"],
        lol_revision_date=lol_summoner["revision_date"],
        lol_summoner_level=lol_summoner["summoner_level"],
        league_of_legends_account=account,
    )
    db.add(summoner)
    db.commit()
    db.refresh(account)
    return account
