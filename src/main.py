import uvicorn
from fastapi import FastAPI

from src.routes import sightseeings_routes
from src.database.models import Base
from src.dependency_injection.di import get_configuration, get_engine


Base.metadata.create_all(bind=get_engine(get_configuration()))

app = FastAPI()

app.include_router(sightseeings_routes.router, prefix='/api')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)