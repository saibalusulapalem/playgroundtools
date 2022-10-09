import pytest


@pytest.fixture
def raw_config():
    """Represents the JSON-decoded config.json file."""
    return {
        "console": {
            "folders": [],
            "files": {"main.py": ["print('Hello, World!')"]},
            "lib": [],
            "module": "main",
            "args": [],
        },
        "api": {
            "folders": ["api"],
            "files": {
                ".env": [
                    "SECRET_KEY='secret_key'",
                    "API_VERSION=1.0.0",
                    "DEBUG=false",
                ],
                "main.py": [
                    "from fastapi import FastAPI",
                    "",
                    "",
                    "app = FastAPI()",
                    "",
                    "",
                    "@app.get('/')",
                    "def root():",
                    "    pass",
                ],
                "reset.py": [
                    "from faker import Faker",
                    "from sqlalchemy import create_engine",
                    "from sqlalchemy.orm import sessionmaker",
                    "",
                    "# Insert code to generate dummy data here",
                ],
                "api/config.py": [
                    "from pydantic import BaseSettings",
                    "",
                    "",
                    "class Settings(BaseSettings):",
                    "    secret_key: str",
                    "    api_version: str",
                    "    debug: bool",
                    "",
                    "    class Config:",
                    "        env_file = '.env'",
                ],
                "api/crud.py": [
                    "from sqlalchemy.orm import Session",
                    "",
                    "",
                    "# Define CRUD operations here",
                ],
                "api/database.py": [
                    "from sqlalchemy import create_engine",
                    "from sqlalchemy.ext.declarative import declarative_base",
                    "from sqlalchemy.orm import sessionmaker",
                    "",
                    "from .config import Settings",
                    "",
                    "",
                    "settings = Settings()",
                    "engine = create_engine(",
                    "    url=DB_URL,",
                    "    connect_args={'check_same_thread': False},",
                    "    echo=settings.debug,",
                    ")",
                    "",
                    "SessionLocal = sessionmaker(",
                    "    bind=engine,",
                    "    autocommit=False,",
                    "    autoflush=False",
                    ")",
                    "",
                    "Base = declarative_base()",
                ],
                "api/deps.py": [
                    "from functools import lru_cache",
                    "",
                    "from .config import Settings",
                    "from .database import SessionLocal",
                    "",
                    "",
                    "def get_db():",
                    "    session = SessionLocal()",
                    "    try:",
                    "        yield session",
                    "    finally:",
                    "        session.close()",
                    "",
                    "",
                    "@lru_cache",
                    "def get_settings():",
                    "    return Settings()",
                ],
                "api/models.py": [
                    "from sqlalchemy import Column, ForeignKey, Integer, String",
                    "from sqlalchemy.orm import relationship",
                    "",
                    "from .database import Base",
                    "",
                    "",
                    "# Define DB models here",
                ],
                "api/schemas.py": [
                    "from pydantic import BaseModel",
                    "",
                    "",
                    "# Define Pydantic schemas here",
                ],
                "api/__init__.py": [],
            },
            "lib": [
                "fastapi",
                "uvicorn",
                "httpie",
                "pydantic",
                "python-dotenv",
                "sqlalchemy",
                "faker",
                "pyjwt",
            ],
            "module": "uvicorn",
            "args": ["main:app", "--reload"],
        },
        "db": {
            "folders": [],
            "files": {
                "main.py": [
                    "from sqlalchemy import create_engine",
                    "from sqlalchemy.orm import sessionmaker",
                    "",
                    "",
                    "DB_URL = 'sqlite:///database.db'",
                    "engine = create_engine(url=DB_URL)",
                    "Session = sessionmaker(bind=engine)",
                ],
                "models.py": [
                    "from sqlalchemy import Column, Integer, ForeignKey, Unicode",
                    "from sqlalchemy.ext.declarative import declarative_base",
                    "from sqlalchemy.orm import relationship",
                    "",
                    "",
                    "Base = declarative_base()",
                    "",
                    "Base.metadata.create_all()",
                ],
            },
            "lib": ["sqlalchemy", "faker"],
            "module": "main",
            "args": [],
        },
        "http": {
            "folders": [],
            "files": {
                "main.py": [
                    "import requests",
                    "from bs4 import BeautifulSoup",
                    "",
                    "",
                    "# Make some requests here...",
                ]
            },
            "lib": ["requests", "beautifulsoup4"],
            "module": "main",
            "args": [],
        },
        "jupyter": {
            "folders": [],
            "files": {
                "dataprep.ipynb": [
                    "{",
                    ' "cells": [',
                    "  {",
                    '   "cell_type": "code",',
                    '   "execution_count": null,',
                    '   "metadata": {},',
                    '   "outputs": [],',
                    '   "source": []',
                    "  }",
                    " ],",
                    ' "metadata": {},',
                    ' "nbformat": 4,',
                    ' "nbformat_minor": 1',
                    "}",
                ],
                "analysis.ipynb": [
                    "{",
                    ' "cells": [',
                    "  {",
                    '   "cell_type": "code",',
                    '   "execution_count": null,',
                    '   "metadata": {},',
                    '   "outputs": [],',
                    '   "source": []',
                    "  }",
                    " ],",
                    ' "metadata": {},',
                    ' "nbformat": 4,',
                    ' "nbformat_minor": 1',
                    "}",
                ],
            },
            "lib": [
                "jupyter",
                "jupyterlab",
                "numpy",
                "pandas",
                "matplotlib",
                "faker",
                "arrow",
            ],
            "module": "jupyter",
            "args": ["notebook", "analysis.ipynb"],
        },
    }
