import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.dev"))

API_TOKEN=env("API_TOKEN")
GROUP_ID=env("GROUP_ID")
