import uvicorn
from fastapi import FastAPI

from src.routes import sightseeings_routes
from src.database.models import Base
from src.dependency_injection.di import get_configuration, get_engine


app = FastAPI()

app.include_router(sightseeings_routes.router, prefix='/api')


if __name__ == "__main__":
    # When running as a script we ensure DB is created using the configured engine.
    engine = get_engine(get_configuration())
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)