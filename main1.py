from fastapi import FastAPI
from databases import Database

DATABASE_URL = "postgresql://postgres:@@lc717283@localhost:5432/postgres"
database = Database(DATABASE_URL)
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/swim_rank")
async def read_swim_rank():
    query = "SELECT * FROM swim_rank LIMIT 10"
    results = await database.fetch_all(query)
    return results

