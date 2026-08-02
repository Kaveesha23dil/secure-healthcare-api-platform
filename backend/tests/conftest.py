import sys
from collections.abc import Callable, Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).parents[1]))
from app.api.dependencies.auth import get_current_user
from app.core.security import AuthenticatedUser
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from tests.factories import create_fictional_data


@pytest.fixture
def db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    local = sessionmaker(bind=engine, expire_on_commit=False)
    session = local()
    create_fictional_data(session)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_db
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def authenticate() -> Generator[Callable[[str, set[str], set[str]], None], None, None]:
    def set_actor(subject: str, roles: set[str], scopes: set[str]) -> None:
        actor = AuthenticatedUser(subject, frozenset(roles), frozenset(scopes))
        app.dependency_overrides[get_current_user] = lambda: actor

    yield set_actor
    app.dependency_overrides.pop(get_current_user, None)
