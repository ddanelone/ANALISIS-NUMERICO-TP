from fastapi import FastAPI
from routers import raices
from routers import gases 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Rutas
app.include_router(raices.router)
app.include_router(gases.router)

# Configuración de CORS ampliada
origins = [
    "http://localhost:3000",                          # local dev
    "http://sd-4140038-h00002.ferozo.net",            # sin www
    "http://www.sd-4140038-h00002.ferozo.net",        # con www
    "https://sd-4140038-h00002.ferozo.net",           # https sin www
    "https://www.sd-4140038-h00002.ferozo.net",       # https con www
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # listado seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
