from src.db.database import engine
from src.db.models import Base


def init_db():
    Base.metadata.create_all(engine)
    print("[INFO] tables created")


if __name__ == "__main__":
    init_db()
