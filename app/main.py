from fastapi import FastAPI

stock_api = FastAPI()


@stock_api.get("/")
async def root():
    return {"message": "Hello World"}
