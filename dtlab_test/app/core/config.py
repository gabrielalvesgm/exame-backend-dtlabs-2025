import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi definida!")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
