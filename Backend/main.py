from fastapi import FastAPI
from routers.tp3 import gases, raices
from fastapi.middleware.cors import CORSMiddleware

# Routers TP1
from routers.tp1 import inciso_1 as tp1_inciso_1
from routers.tp1 import inciso_2 as tp1_inciso_2
from routers.tp1 import inciso_3
from routers.tp1 import inciso_4

# Routers TP2
from routers.tp2 import inciso_1 as tp2_inciso_1
from routers.tp2 import inciso_2 as tp2_inciso_2
from routers.tp2 import inciso_3 as tp2_inciso_3

# CORS
origins = [
    "http://localhost:3000",
    "http://sd-4140038-h00002.ferozo.net",
    "http://www.sd-4140038-h00002.ferozo.net",
    "https://sd-4140038-h00002.ferozo.net",
    "https://www.sd-4140038-h00002.ferozo.net",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(tp1_inciso_1.router, prefix="/api/tp1")
app.include_router(tp1_inciso_2.router, prefix="/api/tp1")
app.include_router(inciso_3.router, prefix="/api/tp1")
app.include_router(inciso_4.router, prefix="/api/tp1")
app.include_router(tp2_inciso_1.router, prefix="/api/tp2")
app.include_router(tp2_inciso_2.router, prefix="/api/tp2")
app.include_router(tp2_inciso_3.router, prefix="/api/tp2")
app.include_router(raices.router, prefix="/api/tp3")
app.include_router(gases.router, prefix="/api/tp3")


