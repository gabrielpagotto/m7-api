from pydantic import BaseModel


class RiotAccountResponse(BaseModel):
    puuid: str
    game_name: str
    tag_line: str


class RiotSummonerResponse(BaseModel):
    id: str
    account_id: str
    puuid: str
    profile_icon_id: int
    revision_date: int
    summoner_level: int
