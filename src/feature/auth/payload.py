from pydantic import BaseModel, EmailStr, field_validator, Field


class SigninPayload(BaseModel):
    email: EmailStr
    password: str


class SignupPayload(BaseModel):
    name: str = Field(min_length=4)
    email: EmailStr
    password: str
    password_confirmation: str

    @field_validator("password")
    def validate_password_strength(cls, value):
        password_min_len = 6
        if len(value) < password_min_len:
            raise ValueError(f"Password must be at least {password_min_len} characters long")
        return value

    @field_validator("password_confirmation")
    def passwords_match(cls, value, validation_info):
        if "password" in validation_info.data and value != validation_info.data["password"]:
            raise ValueError("Passwords do not match.")
        return value


class RefreshPayload(BaseModel):
    refresh_token: str
