from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from src.database.connection import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
if __name__ == "__main__":
    # Test the database connection
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        db.close()