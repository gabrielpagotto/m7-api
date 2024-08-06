from pydantic import BaseModel


class SetRiotPuuidPayload(BaseModel):
    puuid: str
