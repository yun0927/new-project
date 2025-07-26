# models.py
from sqlalchemy import Table, Column, Integer, String, MetaData, Float

metadata = MetaData()

swim_rank = Table(
    "swim_rank",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("event", String),
    Column("age", String),
    Column("gender", String),
    Column("time", String),
    Column("time_sec", Float),
    Column("meet", String),
)
