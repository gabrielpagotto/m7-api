import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    phone: str = None
    is_email_verified: bool
    is_admin: bool
    league_of_legends_account: Optional["LeagueOfLegendsAccountResponse"]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class LeagueOfLegendsAccountResponse(BaseModel):
    id: uuid.UUID
    lol_game_name: str
    lol_tag_line: str
    lol_puuid: str
    user_id: uuid.UUID = None
    league_of_legends_summoner: "LeagueOfLegendsSummonerResponse" = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class LeagueOfLegendsSummonerResponse(BaseModel):
    id: uuid.UUID
    lol_id: str
    lol_account_id: str
    lol_puuid: str
    lol_profile_icon_id: int
    lol_revision_date: int
    lol_summoner_level: int
    league_of_legends_account_id: uuid.UUID = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
