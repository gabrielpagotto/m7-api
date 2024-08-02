from pydantic import BaseModel


class AuthenticationResponse(BaseModel):
    access_token: str
    refresh_token: str
