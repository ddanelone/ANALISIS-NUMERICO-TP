from fastapi import FastAPI
from routers import raices
from routers import gases 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(raices.router)
app.include_router(gases.router) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # O "*", si estás probando
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)