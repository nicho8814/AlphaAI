from database.connection import engine
from database.models import Base

print("Creating database...")

Base.metadata.create_all(bind=engine)

print("Database ready!")