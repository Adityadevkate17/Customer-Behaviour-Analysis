
import os
import time
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 15}
)


def load_data(max_retries=3):

    query = text("SELECT * FROM public.customer")

    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                df = pd.read_sql(query, conn)

            return df

        except SQLAlchemyError as e:

            print(f"Database connection attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                time.sleep(2)

            else:
                raise
