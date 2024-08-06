from pydantic import BaseModel, EmailStr, field_validator, Field


class SigninPayload(BaseModel):
    email: EmailStr
    password: str


class SignupPayload(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password_strength(cls, value):
        password_min_len = 6
        if len(value) < password_min_len:
            raise ValueError(f"Password must be at least {password_min_len} characters long")
        return value


class RefreshPayload(BaseModel):
    refresh_token: str
