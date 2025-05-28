from fastapi import FastAPI
from app.api.v1 import routes
from app.config.cors import add_cors

app = FastAPI()
app.include_router(routes.router)
add_cors(app)
