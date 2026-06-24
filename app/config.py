import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
