from sqlmodel import SQLModel
from app.db.session import engine
from app.models.user import User
from app.models.task import Task

def init_db():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db() 