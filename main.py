from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat
from app.db.mysql import MySQLPool
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await MySQLPool.close()


app = FastAPI(
    title="Aros Business Intelligence",
    description="API Agente BI conversacional para restaurantes. Responde preguntas de negocio en lenguaje natural consultando la base de datos.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz - información de la API"""
    return {
        "name": "Aros Business Intelligence",
        "version": "1.0.0",
        "description": "API Agente BI conversacional para restaurantes",
    }


@app.get("/health", tags=["Health"])
def health():
    """Health check para monitoring y readiness probes"""
    return {"status": "healthy"}
