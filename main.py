from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core import database
from src.feature.auth.handler import router as auth_router
from src.feature.user.handler import router as user_router
from src.feature.riot.handler import router as riot_router

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="M7 Academy")
app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(riot_router)
