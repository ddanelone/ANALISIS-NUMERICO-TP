from fastapi import FastAPI
from routers import endpoints

app = FastAPI()

# Registrar las rutas definidas en el router
app.include_router(endpoints.router)
