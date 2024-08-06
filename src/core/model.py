import uuid
from src.core.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func, Integer, BigInteger
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
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


class LeagueOfLegendsAccount(Base):
    __tablename__ = "league_of_legends_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    lol_game_name = Column(String())
    lol_tag_line = Column(String())
    lol_puuid = Column(String())
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(6), nullable=True, default=None)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", uselist=False, back_populates="league_of_legends_account")
    league_of_legends_summoner: Mapped["LeagueOfLegendsSummoner"] = relationship(
        "LeagueOfLegendsSummoner", uselist=False, back_populates="league_of_legends_account", cascade='all'
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __str__(self):
        return f"{self.lol_tag_line} {self.lol_game_name}"


class LeagueOfLegendsSummoner(Base):
    __tablename__ = "league_of_legends_summoners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    lol_id = Column(String())
    lol_account_id = Column(String())
    lol_puuid = Column(String())
    lol_profile_icon_id = Column(Integer())
    lol_revision_date = Column(BigInteger())
    lol_summoner_level = Column(Integer())
    league_of_legends_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("league_of_legends_accounts.id"),
    )
    league_of_legends_account: Mapped["LeagueOfLegendsAccount"] = relationship(
        "LeagueOfLegendsAccount", back_populates="league_of_legends_summoner"
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
