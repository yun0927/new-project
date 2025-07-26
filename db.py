# db.py
from databases import Database

DATABASE_URL = "postgresql://postgres:@@lc717283@localhost:5432/postgres"

database = Database(DATABASE_URL)
