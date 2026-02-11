from fastapi import FastAPI, APIRouter
from app.api.v1 import product
from app.core.database import Base,engine
from app.models import productModel
app = FastAPI(title="storeManagement")

Base.metadata.create_all(bind=engine)

app.include_router(product.router,prefix="/app/api/v1")