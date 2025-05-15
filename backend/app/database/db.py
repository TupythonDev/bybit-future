from sqlmodel import create_engine, Session, SQLModel, select
from app.database.models import User, UserRole
from app.utils.security import hash_password
from app.core.config import settings

engine = create_engine(settings.database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        email = "tupython.dev@gmail.com"
        statement = select(User).where(User.email == email)
        has_user = session.exec(statement).first()
        if not has_user:
            user = User(
                email=email,
                password=hash_password("P0rr4vivian-"),
                role=UserRole.ADMIN
            )
            session.add(user)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session
