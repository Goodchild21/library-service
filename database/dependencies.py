import redis
import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_engine(DATABASE_URL)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis_cache"),
    port=int(os.getenv("REDIS_PORT", 6381)),
    db=0,
)
