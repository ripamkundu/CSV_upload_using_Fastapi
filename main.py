from fastapi import FastAPI
from routers.upload import router as uploadAsRouter


app = FastAPI(
    title="Upload CSV",
    description="Upload CSV",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


app.include_router(uploadAsRouter)
