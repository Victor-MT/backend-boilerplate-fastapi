from fastapi import FastAPI
from api.routers import user, upload
from fastapi.middleware.cors import CORSMiddleware
from core.middlewares import add_custom_logger

app = FastAPI()
prefix = '/api'

# Configuração para permitir CORS de qualquer origem
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(add_custom_logger)

app.include_router(user.router, prefix=prefix)
app.include_router(upload.router, prefix=prefix)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)