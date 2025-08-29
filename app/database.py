from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
import shutil


def _resolve_database_url() -> str:
	# 1) Allow override via env (e.g., Postgres for production)
	env_url = os.getenv("DATABASE_URL")
	if env_url:
		return env_url

	# 2) On Vercel/serverless, use /tmp which is the only writable path
	#    Copy bundled sqlite file to /tmp on cold start so writes succeed
	if os.getenv("VERCEL") == "1" or os.getenv("VERCEL_ENV"):
		project_root = os.path.dirname(os.path.dirname(__file__))  # backend/
		source_sqlite = os.path.join(project_root, "lance.db")
		tmp_sqlite = "/tmp/lance.db"
		try:
			if os.path.exists(source_sqlite) and not os.path.exists(tmp_sqlite):
				shutil.copyfile(source_sqlite, tmp_sqlite)
		except Exception:
			# If copy fails, fallback to empty db at /tmp
			pass
		return "sqlite:////tmp/lance.db"

	# 3) Local/dev default: keep sqlite in project directory
	return "sqlite:///./lance.db"


SQLALCHEMY_DATABASE_URL = _resolve_database_url()

engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# FastAPI dependency to provide a DB session per request

def get_db() -> Generator:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
