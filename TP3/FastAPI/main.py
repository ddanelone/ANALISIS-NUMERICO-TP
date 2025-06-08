from fastapi import FastAPI
from routers import raices
from routers import gases 

app = FastAPI()
app.include_router(raices.router)
app.include_router(gases.router) 