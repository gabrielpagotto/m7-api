import uuid, enum
from src.core.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func, Enum as SQLAEnum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String())
    email: str = Column(String(), unique=True, index=True)
    hashed_password = Column(String())
    phone_number = Column(String(), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    email_verification_code = Column(String(6), nullable=True, default=None)
    league_of_legends_account: Mapped["LeagueOfLegendsAccount"] = relationship(
        "LeagueOfLegendsAccount", uselist=False, back_populates="user"
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __str__(self):
        return self.email


class LeagueOfLegendsTagLine(enum.Enum):
    BR1 = "br1"


class LeagueOfLegendsAccount(Base):
    __tablename__ = "league_of_legends_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    lol_account_id = Column(String())
    lol_game_name = Column(String())
    lol_tag_line = Column(SQLAEnum(LeagueOfLegendsTagLine), nullable=True)
    lol_puuid = Column(String())
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(6), nullable=True, default=None)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="league_of_legends_account")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __str__(self):
        return f"{self.lol_tag_line} {self.lol_game_name}"


class LeagueOfLegendsSummoner(Base):
    __tablename__ = "league_of_legends_summoners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
